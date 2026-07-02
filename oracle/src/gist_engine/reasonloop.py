"""ReasonLoop: stitch the GIST mechanism into a model's reasoning chain.

Two modes, one mechanism:

  pre-gate   an instant candidate answer is decomposed into claims, fed
             through a compressed lattice session, and gated *before*
             emission: yes -> emit, no -> withhold (with why), maybe ->
             the asks become the model's next reasoning targets.

  in-chain   the reasoning chain itself runs through the lattice as it is
             produced: every step the model emits is superposed as evidence,
             and the engine feeds back a ternary go-signal, contradiction
             holds (VDR), and open asks. The harness injects
             `steering_block()` into the model's context every few steps -
             the chain and the field co-evolve. The model reasons; the
             lattice remembers, checks debt, and says what is still open.

The feedback protocol is deliberately the same ternary bridge everywhere:

    proceed = "yes"    the chain is coherent and decisive so far
    proceed = "maybe"  open aperture: keep reasoning (asks say where)
    proceed = "no"     unresolved coherence debt: the chain has latched
                       contradictions it must repair before concluding

What this is (honestly): a structural coherence, contradiction-debt, and
saturation governor for chain-of-thought, with a verifiable ledger of the
whole reasoning episode. What it is not: a truth oracle - polarity/salience
of steps come from the host or the deterministic projector, and semantic
grounding remains the model's job. The mechanism guarantees the *shape* of
the episode: balanced commitments, attributed contradictions, explicit
open questions, gated conclusions, replayable record.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Any, Sequence

from .bridge import address_of_index
from .engine import GistConfig, GistEngine
from .ports import Atom
from .verdict import (
    Verdict,
    _aggregate_trit,
    conclude,
    verdict,
    verdict_config,
)
from .walks import to_word


@dataclass
class StepFeedback:
    proceed: str                  # 'yes' | 'maybe' | 'no'
    trit: int                     # +1 / 0 / -1 aggregate-so-far
    S: float
    cycle: int
    contradictions: list[str] = dc_field(default_factory=list)
    asks: list[str] = dc_field(default_factory=list)
    saturated_scopes: int = 0
    open_scopes: int = 0

    def to_json(self) -> dict[str, Any]:
        return {
            "proceed": self.proceed,
            "trit": self.trit,
            "S": round(self.S, 4),
            "cycle": self.cycle,
            "contradictions": self.contradictions,
            "asks": self.asks,
            "saturated_scopes": self.saturated_scopes,
            "open_scopes": self.open_scopes,
        }


class ReasonLoop:
    """A live lattice session wrapped around a reasoning episode."""

    def __init__(
        self,
        prompt: str,
        session_id: str | None = None,
        config: GistConfig | None = None,
        ledger_path: str | None = None,
        step_every: int = 1,
    ):
        self.engine = GistEngine(
            prompt=prompt,
            session_id=session_id,
            config=config or verdict_config(),
            ledger_path=ledger_path,
        )
        self.step_every = max(1, step_every)
        self._feeds_since_step = 0

    # -- in-chain mode -------------------------------------------------------

    def feed(
        self,
        step_text: str,
        polarity: float | None = None,
        salience: float | None = None,
        address: tuple[int, int, int] | None = None,
    ) -> StepFeedback:
        """Superpose one reasoning step into the field and read the go-signal.

        polarity: the step's stance toward the episode's prompt/claim
        (+ supports, - contradicts, 0 exploratory/orthogonal). When the host
        cannot supply it, the deterministic projector fills it (documented
        heuristic; exploratory steps are well served by polarity 0, which
        superposes at the crossing and holds the aperture open).
        """
        self.engine.ingest(
            Atom(content=step_text, polarity=polarity, salience=salience,
                 address=address)
        )
        self._feeds_since_step += 1
        if self._feeds_since_step >= self.step_every:
            self.engine.step()
            self._feeds_since_step = 0
        return self._feedback()

    def _feedback(self) -> StepFeedback:
        eng = self.engine
        agg_trit, _amp = _aggregate_trit(eng)
        S = eng.S_history[-1] if eng.S_history else 0.0

        contradictions = []
        for e in eng.ledger.of_kind("vdr_hint"):
            p = e.payload
            if p.get("action") == "seek_counter_evidence":
                slot = p.get("slot")
                if slot is not None and not any(
                    t != 0 for t in eng.slots[slot].last_word
                ):
                    contradictions.append(
                        f"scope {address_of_index(slot)}: {p['detail']}"
                    )
        asks = [it.query_hint for it in eng.intents.values()]
        saturated = sum(1 for s in eng.slots.values() if s.saturated)
        open_scopes = sum(
            1 for s in eng.slots.values()
            if s.atom_count > 0 and not s.saturated
        )
        if contradictions:
            proceed = "no"
        elif agg_trit != 0 and S >= eng.config.thresholds.tau_S and not asks:
            proceed = "yes"
        else:
            proceed = "maybe"
        return StepFeedback(
            proceed=proceed,
            trit=agg_trit if proceed == "yes" else (0 if proceed == "maybe" else -1),
            S=S,
            cycle=eng.cycle,
            contradictions=contradictions,
            asks=asks,
            saturated_scopes=saturated,
            open_scopes=open_scopes,
        )

    def steering_block(self, max_scopes: int = 6) -> str:
        """A compressed field-state block for injection into model context.

        The frontier move: the model reasons *with* the lattice's live state
        in-context - decisive scopes, open apertures, contradiction debt,
        and the ternary go-signal - a few hundred characters, ledger-backed.
        """
        eng = self.engine
        fb = self._feedback()
        lines = [
            f"[GIST field | cycle {eng.cycle} | S={fb.S:.2f} | "
            f"go={fb.proceed} | scopes: {fb.saturated_scopes} settled, "
            f"{fb.open_scopes} open]"
        ]
        active = [
            (i, s) for i, s in eng.slots.items()
            if s.atom_count > 0 and s.metrics is not None
        ]
        active.sort(key=lambda kv: kv[1].metrics.coverage
                    * kv[1].metrics.coherence, reverse=True)
        axes = eng.config.axes
        for i, s in active[:max_scopes]:
            q = address_of_index(i)
            state = "settled" if s.saturated else (
                "asking" if s.open_intent else "forming")
            lines.append(
                f"  scope ({axes[0]}={q[0]},{axes[1]}={q[1]},{axes[2]}={q[2]}) "
                f"word={to_word(s.last_word)} {state}"
            )
        for c in fb.contradictions[:3]:
            lines.append(f"  DEBT: {c}")
        for a in fb.asks[:3]:
            lines.append(f"  OPEN: {a}")
        return "\n".join(lines)

    # -- conclusion gating -----------------------------------------------------

    def gate_answer(self, max_cycles: int = 16) -> Verdict:
        """Attempt the gated conclusion of the episode's lattice.

        Delegates to verdict.conclude(): the identical Pearl-symmetric rule
        (with the mirror ¬C session) that governs the one-shot tool and MCP
        surfaces. 'maybe' verdicts carry the asks the model should reason
        about next; 'no' carries the mirror's gated support and the latched
        contradiction holds.
        """
        return conclude(self.engine, max_cycles=max_cycles)


def pre_gate(
    candidate_answer: str,
    claims: Sequence[dict[str, Any]] | None = None,
    prompt: str | None = None,
    session_id: str | None = None,
) -> Verdict:
    """Pre-gate mode: test an instant candidate answer before emission.

    `claims` are the answer's decomposed claims as atom specs (the host or
    model supplies stance); without them, the answer's lines are projected
    deterministically. Returns the standard ternary Verdict: yes -> emit,
    no -> withhold and repair (holds say where), maybe -> the asks are the
    reasoning targets to pursue before answering.
    """
    return verdict(
        claim=prompt or candidate_answer,
        atoms=claims,
        transcript=None if claims else candidate_answer,
        session_id=session_id,
    )
