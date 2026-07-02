"""The verdict bridge: GIST compressed to one architecture-agnostic call.

Any model, agent framework, or harness asks one question - "does the
evidence carry this claim?" - and receives the balanced-ternary answer the
calculus was built around:

    yes    +1   decisive support latched behind the gate's guards
    no     -1   decisive contradiction latched behind the same guards
    maybe   0   the live crossing: the aperture is open, and the response
                carries exactly what would settle it (the engine's asks)

"maybe" is not failure or absence - it is the calculus's equilibrium
crossing, the state of maximal openness to relation. A harness in an
iterative loop treats it as "keep going, here is what I need"; the asks are
ready-made retrieval prompts.

Three integration surfaces, one mechanism:

  1. tool call (any architecture):
         from gist_engine.verdict import TOOL_SPEC, as_tool_call
         # register TOOL_SPEC with your model; dispatch calls:
         result_json = as_tool_call(arguments_json)

  2. MCP: `python3 -m gist_engine.mcp_server` (see mcp_server.py)

  3. direct stitch (a coding harness, ~6 lines):
         from gist_engine.verdict import verdict, Atom
         v = verdict("the refactor preserves behavior",
                     atoms=[Atom(content="all 74 tests pass", polarity=0.9,
                                 salience=0.9)])
         if v.decision == "yes": proceed()
         elif v.decision == "no": stop(v.why)
         else: iterate(v.asks)

Honesty contract: `basis` distinguishes a "gated-release" verdict (the full
seven-check gate passed on the occupied scope; stamp included) from a
"board-read" verdict (the field's current state, gate not yet passed).
Decisions are never manufactured: a yes/no requires a latched, admissible,
guard-accepted aggregate; anything less is maybe.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field as dc_field
from typing import Any, Iterable, Sequence

from .algebra import corefold_2_to_1, corefold_3_to_2, interfere, trit
from .bridge import address_of_index
from .engine import GistConfig, GistEngine
from .gate import GateThresholds
from .ports import Atom, ProjectedAtom
from .walks import classify, to_word


@dataclass
class Verdict:
    decision: str                 # 'yes' | 'no' | 'maybe'
    trit: int                     # +1 | -1 | 0  (the balanced-ternary bridge)
    confidence: float             # [0, 1]
    basis: str                    # 'gated-release' | 'board-read'
    S: float
    tier: str
    asks: list[str] = dc_field(default_factory=list)
    holds: list[str] = dc_field(default_factory=list)
    why: list[dict[str, Any]] = dc_field(default_factory=list)
    session_id: str = ""
    stamp: str | None = None
    coordinate: dict[str, Any] | None = None
    cycles: int = 0
    ledger_events: int = 0

    def to_json(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "trit": self.trit,
            "confidence": round(self.confidence, 4),
            "basis": self.basis,
            "S": round(self.S, 4),
            "tier": self.tier,
            "asks": self.asks,
            "holds": self.holds,
            "why": self.why,
            "session_id": self.session_id,
            "stamp": self.stamp,
            "coordinate": self.coordinate,
            "cycles": self.cycles,
            "ledger_events": self.ledger_events,
        }


def verdict_config() -> GistConfig:
    """The compressed realization for one-shot verdict sessions."""
    return GistConfig(
        gate_scope="occupied",
        patience=2,
        retrieval_budget=6,
        thresholds=GateThresholds(hysteresis=2),
    )


def _atoms_from_specs(specs: Iterable[dict[str, Any] | Atom]) -> list[Atom]:
    out: list[Atom] = []
    for s in specs:
        if isinstance(s, Atom):
            out.append(s)
            continue
        out.append(
            Atom(
                content=str(s["content"]),
                polarity=s.get("polarity"),
                salience=s.get("salience"),
                address=tuple(s["address"]) if s.get("address") else None,
                vector=tuple(s["vector"]) if s.get("vector") else None,
                provenance=dict(s.get("provenance", {})),
            )
        )
    return out


def _atoms_from_transcript(transcript: str) -> list[Atom]:
    """Heuristic adapter (documented as such): each non-empty line becomes an
    atom; polarity/salience/address are hash-projected deterministically. A
    host with real stance/salience information should pass atoms explicitly -
    this adapter exists so the bridge is never blocked on parsing."""
    atoms = []
    for line in transcript.splitlines():
        line = line.strip()
        if line:
            atoms.append(Atom(content=line))
    return atoms


def _aggregate_trit(engine: GistEngine) -> tuple[int, float]:
    """The board-level conclusion: ⊞ over occupied write cones, ∂ to the
    singular, quantized. Returns (trit, amplitude of the singular)."""
    cones: list[list] = [[], [], []]
    for i, s in engine.slots.items():
        if s.atom_count == 0:
            continue
        vals = engine.field.modules[engine._slot_name(i)].write_values()
        for pos in range(3):
            if abs(vals[pos]) > 0:
                cones[pos].append(vals[pos])
    read = [
        interfere(*vs) / len(vs) if vs else 0j
        for vs in cones
    ]
    singular = corefold_2_to_1(corefold_3_to_2(read))
    return trit(singular, engine.field.deadband), abs(singular)


def derive_verdict(engine: GistEngine) -> Verdict:
    """Bridge a live engine's state to a ternary Verdict.

    Decision rule (mechanism-derived, never manufactured): yes/no requires a
    decisive aggregate singular (trit ±1), global agreement S >= tau_S, no
    unresolved balance-violation holds among occupied slots, and at least
    one contributing slot; everything else is maybe with asks. Confidence =
    S x mean coverage of contributing slots, discounted when the gate has
    not released.
    """
    cfg = engine.config
    agg_trit, _amp = _aggregate_trit(engine)
    S = engine.S_history[-1] if engine.S_history else 0.0
    report = engine.gate_report
    released = engine.release_record is not None

    holds: list[str] = []
    for e in engine.ledger.of_kind("vdr_hint"):
        p = e.payload
        if p.get("action") == "seek_counter_evidence":
            slot = p.get("slot")
            if slot is not None and not any(
                t != 0 for t in engine.slots[slot].last_word
            ):
                holds.append(
                    f"slot {slot} {tuple(address_of_index(slot))}: {p['detail']}"
                )
    holds = list(dict.fromkeys(holds))

    asks: list[str] = [it.query_hint for it in engine.intents.values()]
    if report is not None and not report.eligible:
        asks.extend(
            f"gate check '{c.name}' unmet: {c.detail}"
            for c in report.checks if not c.passed
        )

    contributing = report.contributing if report else []
    mean_cov = (
        sum(engine.slots[s].metrics.coverage for s in contributing)
        / len(contributing) if contributing else 0.0
    )

    decisive = (
        agg_trit != 0
        and S >= cfg.thresholds.tau_S
        and not holds
        and bool(contributing)
    )
    decision = ("yes" if agg_trit > 0 else "no") if decisive else "maybe"
    bridge_trit = agg_trit if decisive else 0
    confidence = max(0.0, min(1.0, S * mean_cov * (1.0 if released else 0.85)))
    if decision == "maybe":
        confidence = min(confidence, 0.5)

    why = []
    for s in sorted(
        contributing,
        key=lambda i: (engine.slots[i].metrics.coverage
                       * engine.slots[i].metrics.coherence),
        reverse=True,
    )[:5]:
        st = engine.slots[s]
        q = address_of_index(s)
        why.append(
            {
                "slot": s,
                "axes": {cfg.axes[k]: q[k] for k in range(3)},
                "word": to_word(st.last_word),
                "tier": classify(st.last_word),
                "metrics": st.metrics.to_json() if st.metrics else None,
            }
        )

    release = engine.release_record
    return Verdict(
        decision=decision,
        trit=bridge_trit,
        confidence=confidence,
        basis="gated-release" if released else "board-read",
        S=S,
        tier=(release["tier"] if released
              else (report.headline_tier if report else "inadmissible")),
        asks=asks,
        holds=holds,
        why=why,
        session_id=engine.session_id,
        stamp=release["stamp"] if released else None,
        coordinate=release["coordinate"] if released else None,
        cycles=engine.cycle,
        ledger_events=len(engine.ledger),
    )


def mirror_projected(projected: Iterable[ProjectedAtom]) -> list[ProjectedAtom]:
    """The negation-test geometry: evidence for C becomes evidence against
    ¬C and vice versa. θ -> π − θ (= arccos(−polarity)), polarity negated;
    slot, salience, content, and provenance unchanged."""
    import math

    out = []
    for p in projected:
        out.append(
            ProjectedAtom(
                content=p.content,
                slot=p.slot,
                polarity=-p.polarity,
                salience=p.salience,
                theta=math.pi - p.theta,
                amplitude=p.amplitude,
                provenance=dict(p.provenance),
            )
        )
    return out


def conclude(engine: GistEngine, max_cycles: int = 24) -> Verdict:
    """Run an engine toward conclusion and bridge Pearl-symmetrically.

    The calculus's commit barrier is deliberately asymmetric: assertions
    must lead (a word opening in contraction is coherence debt), so a
    decisively *contradicted* claim can never latch as C. The conclusion is
    made symmetric by construction: when C is not decisively carried, the
    engine's own recorded inputs are mirrored (θ -> π−θ: evidence against C
    becomes evidence for ¬C) into a twin session, and 'no' is a decisive,
    gate-guarded 'yes' on that mirror. If neither direction is decisive the
    answer is maybe, carrying both sessions' asks and holds. This one
    function governs the tool surface, the MCP surface, and the reasoning
    loop identically.
    """
    engine.run(max_cycles=max_cycles)
    primary = derive_verdict(engine)
    if primary.decision == "yes":
        return primary

    # rebuild the evidence geometry from the engine's own input events
    projected = [
        ProjectedAtom(
            content=e.payload["content"],
            slot=e.payload["slot"],
            polarity=e.payload["polarity"],
            salience=e.payload["salience"],
            theta=e.payload["theta"],
            amplitude=e.payload["amplitude"],
            provenance=e.payload.get("provenance", {}),
        )
        for e in engine.ledger.of_kind("atom_queued")
    ]
    if not projected:
        return primary

    mirror = GistEngine(
        prompt=f"NOT({engine.prompt})",
        session_id=f"{engine.session_id}-mirror",
        config=engine.config,
    )
    mirror.ingest_projected(mirror_projected(projected))
    mirror.run(max_cycles=max_cycles)
    mirror_verdict = derive_verdict(mirror)

    if mirror_verdict.decision == "yes":
        # decisive support for ¬C = the gated 'no' on C
        v = mirror_verdict
        return Verdict(
            decision="no",
            trit=-1,
            confidence=v.confidence,
            basis=v.basis,
            S=v.S,
            tier=v.tier,
            asks=v.asks,
            holds=v.holds,
            why=v.why,
            session_id=engine.session_id,
            stamp=v.stamp,
            coordinate=v.coordinate,
            cycles=engine.cycle + v.cycles,
            ledger_events=len(engine.ledger) + v.ledger_events,
        )

    # neither direction decisive: honest maybe with both sessions' guidance
    p = primary
    return Verdict(
        decision="maybe",
        trit=0,
        confidence=min(p.confidence, 0.5),
        basis=p.basis,
        S=p.S,
        tier=p.tier,
        asks=list(dict.fromkeys(p.asks + mirror_verdict.asks)),
        holds=list(dict.fromkeys(p.holds + mirror_verdict.holds)),
        why=p.why or mirror_verdict.why,
        session_id=engine.session_id,
        stamp=None,
        coordinate=None,
        cycles=engine.cycle + mirror_verdict.cycles,
        ledger_events=len(engine.ledger) + mirror_verdict.ledger_events,
    )


def verdict(
    claim: str,
    atoms: Sequence[dict[str, Any] | Atom] | None = None,
    transcript: str | None = None,
    session_id: str | None = None,
    max_cycles: int = 24,
    config: GistConfig | None = None,
    ledger_path: str | None = None,
    projector: Any = None,
) -> Verdict:
    """One-shot ternary verdict on a claim (see `conclude` for the rule)."""
    from .ports import HashProjector

    cfg = config or verdict_config()
    proj = projector or HashProjector()
    specs = _atoms_from_specs(atoms or [])
    if transcript:
        specs.extend(_atoms_from_transcript(transcript))
    projected = [proj.project(a) for a in specs]

    engine = GistEngine(prompt=claim, session_id=session_id, config=cfg,
                        ledger_path=ledger_path)
    if projected:
        engine.ingest_projected(projected)
    return conclude(engine, max_cycles=max_cycles)


# ---------------------------------------------------------------------------
# the architecture-agnostic tool surface
# ---------------------------------------------------------------------------

TOOL_SPEC: dict[str, Any] = {
    "name": "gist_verdict",
    "description": (
        "Test a claim against evidence through the GIST coherence engine "
        "(balanced-ternary, gate-guarded, replay-verifiable). Returns "
        "decision yes/no/maybe with trit +1/-1/0. 'maybe' means the aperture "
        "is open and `asks` lists exactly what evidence would settle it - "
        "fulfill the asks and call again. yes/no are mechanism-derived "
        "(decisive latched aggregate, global agreement, no unresolved "
        "contradiction holds), never guessed."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "claim": {
                "type": "string",
                "description": "The claim/decision to test.",
            },
            "atoms": {
                "type": "array",
                "description": (
                    "Evidence atoms. polarity in [-1,1]: sign and strength "
                    "of support for the claim (+ supports, - contradicts, "
                    "0 orthogonal). salience in [0,1]: evidence weight. "
                    "address: optional [q1,q2,q3] scope, each 0-3. Omitted "
                    "fields are hash-projected deterministically."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "polarity": {"type": "number"},
                        "salience": {"type": "number"},
                        "address": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "minItems": 3,
                            "maxItems": 3,
                        },
                        "provenance": {"type": "object"},
                    },
                    "required": ["content"],
                },
            },
            "transcript": {
                "type": "string",
                "description": (
                    "Optional raw text; each line becomes an atom via the "
                    "deterministic hash projector (heuristic adapter - "
                    "prefer explicit atoms when stance is known)."
                ),
            },
        },
        "required": ["claim"],
    },
}


def as_tool_call(arguments: str | dict[str, Any]) -> str:
    """Pure JSON-in/JSON-out dispatch for any tool-calling architecture."""
    args = json.loads(arguments) if isinstance(arguments, str) else arguments
    v = verdict(
        claim=args["claim"],
        atoms=args.get("atoms"),
        transcript=args.get("transcript"),
        session_id=args.get("session_id"),
    )
    return json.dumps(v.to_json(), ensure_ascii=False)
