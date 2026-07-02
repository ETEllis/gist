"""GistEngine: the executable GIST mechanism.

GIST = Gated Insight Synthesis Topology, instantiated from the BiDi
Coherence-Delta Calculus at the bootstrap arity n = 6 (the bridge64 surface,
2^6 = 4^3 = 64).

One engine = one session = one append-only ledger. The engine is:

  - deterministic: identical inputs (projected atoms, cycle boundaries)
    produce an identical ledger payload stream, so any third party can
    replay-verify a session from the ledger alone (`verify_ledger`);
  - sans-IO: evidence enters through `ingest`/`fulfill`; wants leave as
    intents; no network, no clock in the semantics;
  - subordinate-ready: embed it under any platform via the Python API, the
    JSONL ledger, or the CLI; couple a frontend to `state_json()` /
    `export_replay()`;
  - self-contained: with no ports attached it still runs end-to-end with the
    deterministic HashProjector.

The cycle (one `step()`):

  1. route   drain pending atoms; superpose (⊞) each into its slot's read
             cone by constructive clustering (contradictions cancel);
  2. flow    continuous reduction of the whole field (the corefold pyramid
             channels compute the 3→2→1 distillation);
  3. commit  guarded balanced-ternary commit of every touched slot
             (accepted / held + reason);
  4. measure metrics (coherence, coverage, stability, cf-agreement, lift),
             plateau detection, openness-split saturation:
             plateau + open boundary  -> retrieval intent (the slot's cells
                                         sit at their crossing: the calculus
                                         state of maximal openness to
                                         relation - GIST's "needs evidence");
             plateau + closed boundary -> saturated;
  5. watch   gate evaluation (all seven checks + hysteresis on S);
  6. release when the gate proposes: ladder 64→…→1 (Merkle = ladder tree),
             meta↔aggregate council reconciliation, bridge-coordinate
             decision, HKDF/HMAC decision stamp, release record.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field as dc_field
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import __version__ as _pkg_version
from .algebra import (
    coh,
    coherence_delta,
    corefold_2_to_1,
    corefold_3_to_2,
    interfere,
    kappa,
    phase,
    wrap_angle,
)
from .bridge import BridgeRow, address_of_index, dyadic_of_index, project_trits
from .crypto import (
    decision_stamp,
    gate_challenge,
    merkle_leaf,
    merkle_root,
    session_key,
)
from .field import Cell, Channel, Field, Module
from .gate import GateReport, GateThresholds, evaluate_gate
from .ladder import LadderResult, run_ladder
from .ledger import Ledger
from .metrics import (
    SlotMetrics,
    causal_lift,
    cf_agreement,
    coverage,
    global_agreement,
    slot_coherence,
    slot_openness,
    stability,
)
from .ports import (
    Atom,
    EscalationIntent,
    HashProjector,
    ProjectedAtom,
    Projector,
    RetrievalIntent,
    polarity_to_theta,
)
from .walks import classify, to_word

DEFAULT_AXES = ("temporal", "abstraction", "evidence-type")


def _r(x: float, places: int = 9) -> float:
    """Round floats entering ledger payloads (cross-platform replay hygiene)."""
    return round(x, places)


@dataclass
class GistConfig:
    axes: tuple[str, str, str] = DEFAULT_AXES
    # field realization
    dt: float = 0.125
    gain: float = 1.0
    deadband: float = 0.5
    snap: float = 0.5
    belief_gain: float = 0.5
    amp_relax: float = 0.8
    flow_per_cycle: float = 1.0
    # metrics realization
    coverage_lambda: float = 3.0
    jitter_angle: float = 0.15
    # saturation / retrieval
    plateau_epsilon: float = 0.02
    patience: int = 3
    open_threshold: float = 0.35
    retrieval_budget: int = 16
    escalate_after: int = 2
    # ladder / reconciliation
    ladder_flow: float = 0.5
    recon_weight: float = 0.3
    recon_flow: float = 1.0
    recon_quorum: int = 4
    tau_recon: float = 0.7
    # gate
    thresholds: GateThresholds = dc_field(default_factory=GateThresholds)
    gate_scope: str = "full"       # 'full' (research) | 'occupied' (verdict)
    auto_release: bool = True

    def to_json(self) -> dict[str, Any]:
        d = asdict(self)
        d["thresholds"] = self.thresholds.to_json()
        d["axes"] = list(self.axes)
        return d

    @staticmethod
    def from_json(d: dict[str, Any]) -> "GistConfig":
        d = dict(d)
        th = d.pop("thresholds", None)
        axes = d.pop("axes", list(DEFAULT_AXES))
        cfg = GistConfig(axes=tuple(axes), **d)
        if th:
            cfg.thresholds = GateThresholds(**th)
        return cfg


@dataclass
class SlotState:
    """Book-keeping per lattice slot (all derivable from the ledger)."""

    index: int
    absorbed: float = 0.0
    atom_count: int = 0
    coherence_history: list[float] = dc_field(default_factory=list)
    last_statuses: list[str] = dc_field(default_factory=list)
    saturated: bool = False
    open_intent: str | None = None
    fulfillments: int = 0
    escalated: bool = False
    last_commit_hash: str | None = None
    last_word: tuple[int, ...] = (0, 0, 0, 0, 0, 0)
    last_vdr_word: str | None = None
    metrics: SlotMetrics | None = None


class GistEngine:
    """One GIST session over the 64-slot lattice."""

    def __init__(
        self,
        prompt: str,
        session_id: str | None = None,
        config: GistConfig | None = None,
        projector: Projector | None = None,
        ledger_path: str | Path | None = None,
        _replaying: bool = False,
    ):
        self.prompt = prompt
        self.session_id = session_id or hashlib.sha256(
            prompt.encode("utf-8")
        ).hexdigest()[:12]
        self.config = config or GistConfig()
        self.projector: Projector = projector or HashProjector()
        self.ledger = Ledger(path=ledger_path)
        self.cycle = 0
        self.pending: list[tuple[ProjectedAtom, str]] = []  # (atom, source)
        self.slots: dict[int, SlotState] = {i: SlotState(index=i) for i in range(64)}
        self.S_history: list[float] = []
        self.intents: dict[str, RetrievalIntent] = {}
        self.intents_emitted = 0
        self.gate_report: GateReport | None = None
        self.release_record: dict[str, Any] | None = None
        self.ladder_result: LadderResult | None = None
        self._blocked_leaf_root: str | None = None
        self.field = self._build_field()
        if not _replaying:
            self.ledger.append(
                "session_init",
                {
                    "engine": "gist-engine",
                    "version": _pkg_version,
                    "session_id": self.session_id,
                    "prompt": self.prompt,
                    "config": self.config.to_json(),
                    "axes": list(self.config.axes),
                    "lattice": {"slots": 64, "arity": 6, "bridge": "2^6=4^3"},
                },
            )

    # ------------------------------------------------------------------ #
    # lattice construction
    # ------------------------------------------------------------------ #

    def _slot_name(self, index: int) -> str:
        return f"slot/{dyadic_of_index(index)}"

    def _build_field(self) -> Field:
        c = self.config
        f = Field(
            name=f"gist/{self.session_id}",
            dt=c.dt,
            gain=c.gain,
            deadband=c.deadband,
            snap=c.snap,
            belief_gain=c.belief_gain,
            amp_relax=c.amp_relax,
        )
        for i in range(64):
            name = self._slot_name(i)
            # cells begin at the crossing (θ = π/2): an unformed cell is an
            # open aperture, never an implicit pole commitment
            cells = [Cell(theta=math.pi / 2.0, amp=0.0) for _ in range(6)]
            f.add_module(Module(name=name, cells=cells))
            # the corefold pyramid as channel structure:
            # read (0,1,2) -> dyad (3,5) -> singular (4)
            for src, dst in ((0, 3), (1, 3), (1, 5), (2, 5)):
                f.add_channel(Channel(src=f"{name}:{src}", dst=f"{name}:{dst}",
                                      weight=0.5))
            for src in (3, 5):
                f.add_channel(Channel(src=f"{name}:{src}", dst=f"{name}:4",
                                      weight=0.5))
        return f

    # ------------------------------------------------------------------ #
    # ingestion (ports in)
    # ------------------------------------------------------------------ #

    def _queue(self, projected: ProjectedAtom, source: str) -> None:
        """Record an input atom (ledger event) and queue it for the next cycle.

        atom_queued events are the *input* half of the ledger: replay feeds
        the engine from them (with the projected geometry recorded, replay
        needs no projector), while atom_ingested routing records are derived
        and regenerated by the replayed cycles.

        Inputs are canonicalized here - geometry quantized to the 1e-9
        ledger precision and content truncated to the recorded length - so
        the live run and any replay compute from bit-identical inputs.
        """
        canonical = ProjectedAtom(
            content=projected.content[:240],
            slot=projected.slot,
            polarity=_r(projected.polarity),
            salience=_r(projected.salience),
            theta=_r(projected.theta),
            amplitude=_r(projected.amplitude),
            provenance=dict(projected.provenance),
        )
        self.ledger.append(
            "atom_queued",
            {
                "slot": canonical.slot,
                "content": canonical.content,
                "polarity": canonical.polarity,
                "salience": canonical.salience,
                "theta": canonical.theta,
                "amplitude": canonical.amplitude,
                "provenance": canonical.provenance,
                "source": source,
            },
        )
        self.pending.append((canonical, source))

    def ingest(self, atoms: Atom | Iterable[Atom]) -> list[ProjectedAtom]:
        """Project and queue evidence; processed on the next step()."""
        if isinstance(atoms, Atom):
            atoms = [atoms]
        out = []
        for atom in atoms:
            projected = self.projector.project(atom)
            self._queue(projected, "ingest")
            out.append(projected)
        return out

    def ingest_projected(
        self, projected: Iterable[ProjectedAtom], source: str = "ingest"
    ) -> list[ProjectedAtom]:
        """Queue pre-projected atoms (hosts that carry their own geometry)."""
        out = []
        for p in projected:
            self._queue(p, source)
            out.append(p)
        return out

    def fulfill(self, intent_id: str, atoms: Iterable[Atom]) -> list[ProjectedAtom]:
        """Answer a retrieval intent with new evidence (a host/reactor action)."""
        if intent_id not in self.intents:
            raise KeyError(f"unknown intent {intent_id!r}")
        intent = self.intents[intent_id]
        atoms = list(atoms)
        slot = self.slots[intent.slot]
        slot.fulfillments += 1
        slot.open_intent = None
        slot.saturated = False
        slot.coherence_history.clear()
        slot.last_statuses.clear()
        del self.intents[intent_id]
        self.ledger.append(
            "intent_fulfilled",
            {"intent_id": intent_id, "slot": intent.slot, "atoms": len(atoms)},
        )
        out = []
        for atom in atoms:
            projected = self.projector.project(atom)
            self._queue(projected, f"fulfill:{intent_id}")
            out.append(projected)
        return out

    def open_intents(self) -> list[RetrievalIntent]:
        return list(self.intents.values())

    # ------------------------------------------------------------------ #
    # the cycle
    # ------------------------------------------------------------------ #

    def step(self) -> dict[str, Any]:
        """One full cycle. Returns a cycle summary (also ledgered)."""
        self.cycle += 1
        batch = self.pending
        self.pending = []
        self.ledger.append(
            "cycle_start", {"cycle": self.cycle, "atoms": len(batch)}
        )

        # 1. route + superpose
        touched: set[int] = set()
        for projected, source in batch:
            self._absorb(projected, source)
            touched.add(projected.slot)

        # 2. flow (the pyramid computes; write cones entrain and gain mass)
        self.field.flow(self.config.flow_per_cycle)

        # 3. commit touched slots (and any slot still unsaturated with content)
        active = sorted(
            touched
            | {
                i
                for i, s in self.slots.items()
                if s.atom_count > 0 and not s.saturated
            }
        )
        commits: dict[int, str] = {}
        for i in active:
            commits[i] = self._commit_slot(i)

        # 4. measure + saturate
        for i in active:
            self._measure_slot(i)

        # 5. watch the gate
        report = self._watch_gate()

        summary: dict[str, Any] = {
            "cycle": self.cycle,
            "routed": len(batch),
            "touched": sorted(touched),
            "commits": commits,
            "S": _r(self.S_history[-1]) if self.S_history else 0.0,
            "gate_eligible": bool(report and report.eligible),
            "open_intents": len(self.intents),
        }

        # 6. release path (skip retries while nothing has changed since a
        # reconciliation hold: the reduction is deterministic, so an
        # identical leaf state cannot reconcile differently)
        if report is not None and report.eligible and self.config.auto_release:
            leaf_root = merkle_root(self._leaf_hashes_list())
            if leaf_root != self._blocked_leaf_root:
                release = self._release(report)
                summary["released"] = release is not None
                if release is None:
                    self._blocked_leaf_root = leaf_root
        self.ledger.append("cycle_end", {"cycle": self.cycle,
                                         "summary_S": summary["S"]})
        return summary

    def run(self, max_cycles: int = 64) -> dict[str, Any] | None:
        """Step until release, quiescence, or max_cycles. Returns the release.

        A quiescent field (nothing pending, everything saturated or empty,
        no open intents) is still stepped a few extra times so the gate's
        S-hysteresis window can fill before the loop concludes nothing more
        can change.
        """
        quiescent_streak = 0
        for _ in range(max_cycles):
            if self.release_record is not None:
                break
            quiescent = (
                not self.pending
                and all(
                    s.saturated or s.atom_count == 0 for s in self.slots.values()
                )
                and not self.intents
            )
            self.step()
            if self.release_record is not None:
                break
            if quiescent and not self.pending:
                quiescent_streak += 1
                if quiescent_streak > self.config.thresholds.hysteresis + 1:
                    break
            else:
                quiescent_streak = 0
        return self.release_record

    # ------------------------------------------------------------------ #
    # internals
    # ------------------------------------------------------------------ #

    def _absorb(self, p: ProjectedAtom, source: str) -> None:
        """⊞ an atom into its slot's read cone by constructive clustering.

        Same-commitment evidence merges into one cell (the clustering angle
        π/3 equals the deadband cone: cos(π/3) = deadband = 1/2, so a cluster
        is exactly a commitment class). New clusters fill the triad in
        dialectic order - first the thesis end, then the far (antithesis)
        end, and the middle last - because the corefold pyramid weights the
        middle cell double: the mediating position carries the bridge.
        """
        module = self.field.modules[self._slot_name(p.slot)]
        value = coh(p.amplitude, p.theta)
        read = module.read_cone
        fill_order = (
            [read[0], read[-1], read[len(read) // 2]]
            if len(read) == 3 else list(read)
        )
        # nearest nonempty read cell by phase; open a new cluster if far/empty
        best_i, best_d = None, None
        empty = None
        for i in fill_order:
            cell = module.cells[i]
            if cell.amp <= 1e-12:
                if empty is None:
                    empty = i
                continue
            d = abs(wrap_angle(cell.theta - p.theta))
            if best_d is None or d < best_d:
                best_i, best_d = i, d
        if best_i is None or (empty is not None and (best_d or 0.0) > 1.0472):
            target = empty if empty is not None else read[0]
        else:
            target = best_i
        cell = module.cells[target]
        merged = interfere(cell.value(), value)
        cell.theta = phase(merged) if abs(merged) > 0 else cell.theta
        cell.amp = abs(merged)

        state = self.slots[p.slot]
        state.absorbed += p.amplitude
        state.atom_count += 1
        self.ledger.append(
            "atom_ingested",
            {
                "slot": p.slot,
                "address": list(p.address),
                "cell": target,
                "content_hash": hashlib.sha256(
                    p.content.encode("utf-8")
                ).hexdigest()[:16],
                "content": p.content[:240],
                "polarity": _r(p.polarity),
                "salience": _r(p.salience),
                "theta": _r(p.theta),
                "amplitude": _r(p.amplitude),
                "source": source,
                "provenance": p.provenance,
            },
        )

    def _commit_slot(self, index: int) -> str:
        name = self._slot_name(index)
        result = self.field.commit(name)
        state = self.slots[index]
        entry = self.ledger.append(
            "slot_commit",
            {
                "slot": index,
                "cycle": self.cycle,
                "status": result.status,
                "reason": result.reason,
                "word": result.word,
                "admissible": result.admissible,
                "tier": classify(result.trits),
                "phi_before": _r(result.phi_before),
                "phi_after": _r(result.phi_after),
                "violation_cell": result.violation_cell,
            },
        )
        state.last_statuses.append(f"{result.status}:{result.reason}")
        if len(state.last_statuses) > 8:
            state.last_statuses = state.last_statuses[-8:]
        if result.accepted:
            state.last_commit_hash = entry.hash
            state.last_word = result.trits
            state.last_vdr_word = None
        elif (result.reason == "balance-violation"
              and state.last_vdr_word != result.word):
            # VDR: exact attribution, non-binding hint into the ledger
            # (deduplicated: re-emitted only when the held word changes)
            state.last_vdr_word = result.word
            self.ledger.append(
                "vdr_hint",
                {
                    "slot": index,
                    "action": "seek_counter_evidence",
                    "cell": result.violation_cell,
                    "word": result.word,
                    "detail": (
                        f"cell {result.violation_cell} forces negative "
                        f"coherence debt; contribute opposing or clarifying "
                        f"evidence to axis scope {address_of_index(index)}"
                    ),
                },
            )
        return f"{result.status}:{result.reason}"

    def _measure_slot(self, index: int) -> None:
        c = self.config
        name = self._slot_name(index)
        module = self.field.modules[name]
        state = self.slots[index]
        m = SlotMetrics(
            slot=index,
            coherence=slot_coherence(module),
            coverage=coverage(state.absorbed, c.coverage_lambda),
            stability=stability(self.field, name, c.jitter_angle),
            cf_agreement=cf_agreement(self.field, name),
            causal_lift=causal_lift(self.field, name),
            openness=slot_openness(module, c.deadband),
        )
        state.metrics = m
        state.coherence_history.append(m.coherence)
        if len(state.coherence_history) > 16:
            state.coherence_history = state.coherence_history[-16:]

        plateaued = self._plateaued(state)
        payload = dict(m.to_json())
        payload.update({"cycle": self.cycle, "plateaued": plateaued,
                        "saturated": state.saturated})
        if plateaued and not state.saturated:
            if m.openness > c.open_threshold:
                self._emit_intent(index, m)
            else:
                state.saturated = True
                payload["saturated"] = True
                self.ledger.append(
                    "slot_saturated",
                    {"slot": index, "cycle": self.cycle,
                     "coherence": _r(m.coherence), "openness": _r(m.openness)},
                )
        self.ledger.append("slot_metrics", payload)

    def _plateaued(self, state: SlotState) -> bool:
        c = self.config
        h = state.coherence_history
        if len(h) >= c.patience:
            window = h[-c.patience:]
            if max(window) - min(window) < c.plateau_epsilon:
                return True
        tail = state.last_statuses[-c.patience:]
        return (
            len(tail) >= c.patience
            and all(s == "held:deadband-jitter" for s in tail)
        )

    def _emit_intent(self, index: int, m: SlotMetrics) -> None:
        c = self.config
        state = self.slots[index]
        if state.open_intent is not None:
            return
        if self.intents_emitted >= c.retrieval_budget:
            return
        if state.fulfillments >= c.escalate_after and not state.escalated:
            state.escalated = True
            esc = EscalationIntent(
                intent_id=f"esc/{index}/{self.cycle}",
                slot=index,
                address=address_of_index(index),
                attempts=state.fulfillments,
                openness=m.openness,
            )
            self.ledger.append(
                "escalation_intent",
                {"intent_id": esc.intent_id, "slot": index,
                 "attempts": esc.attempts, "openness": _r(esc.openness)},
            )
        module = self.field.modules[self._slot_name(index)]
        gap_cells = tuple(
            i for i in module.read_cone
            if abs(kappa(module.cells[i].value())) <= self.field.deadband
        )
        q = address_of_index(index)
        axes = self.config.axes
        hint = (
            f"evidence for scope [{axes[0]}={q[0]}, {axes[1]}={q[1]}, "
            f"{axes[2]}={q[2]}]: read cells {list(gap_cells)} sit at their "
            f"crossing (undecided); contribute decisive supporting or "
            f"contradicting atoms"
        )
        intent = RetrievalIntent(
            intent_id=f"ri/{index}/{self.cycle}",
            slot=index,
            address=q,
            openness=m.openness,
            coherence=m.coherence,
            gap_cells=gap_cells,
            query_hint=hint,
            fulfillments=state.fulfillments,
        )
        self.intents[intent.intent_id] = intent
        state.open_intent = intent.intent_id
        self.intents_emitted += 1
        self.ledger.append(
            "retrieval_intent",
            {
                "intent_id": intent.intent_id,
                "slot": index,
                "address": list(q),
                "openness": _r(m.openness),
                "coherence": _r(m.coherence),
                "gap_cells": list(gap_cells),
                "query_hint": hint,
                "budget_remaining": c.retrieval_budget - self.intents_emitted,
            },
        )

    def _watch_gate(self) -> GateReport | None:
        slot_names = [self._slot_name(i) for i in range(64)]
        S = global_agreement(self.field, slot_names, singular_index=4)
        self.S_history.append(S)
        if len(self.S_history) > 64:
            self.S_history = self.S_history[-64:]
        words = {i: s.last_word for i, s in self.slots.items()}
        metrics = {
            i: s.metrics for i, s in self.slots.items() if s.metrics is not None
        }
        report = evaluate_gate(
            slot_words=words,
            slot_metrics=metrics,
            saturated={i for i, s in self.slots.items() if s.saturated},
            S_history=self.S_history,
            thresholds=self.config.thresholds,
            budget_exhausted=self.intents_emitted >= self.config.retrieval_budget
            and not self.intents,
            scope=self.config.gate_scope,
            occupied={i for i, s in self.slots.items() if s.atom_count > 0},
        )
        self.gate_report = report
        self.ledger.append(
            "gate_eval", {"cycle": self.cycle, "report": report.to_json()}
        )
        if report.eligible:
            leaf_root = merkle_root(self._leaf_hashes_list())
            self.ledger.append(
                "gate_proposal",
                {"cycle": self.cycle, "report": report.to_json(),
                 "merkle_leaf_root": leaf_root},
            )
        return report

    def _leaf_hashes(self) -> dict[int, str]:
        out: dict[int, str] = {}
        for i, s in self.slots.items():
            if s.last_commit_hash is not None:
                out[i] = s.last_commit_hash
            else:
                out[i] = merkle_leaf({"slot": i, "void": True})
        return out

    def _leaf_hashes_list(self) -> list[str]:
        h = self._leaf_hashes()
        return [h[i] for i in range(64)]

    # ------------------------------------------------------------------ #
    # release: ladder -> reconciliation -> stamp
    # ------------------------------------------------------------------ #

    def _release(self, report: GateReport) -> dict[str, Any] | None:
        leaf_hashes = self._leaf_hashes()
        leaf_modules = {
            i: self.field.modules[self._slot_name(i)] for i in range(64)
        }
        ladder = run_ladder(
            leaf_modules, leaf_hashes, self.field, self.config.ladder_flow
        )
        self.ladder_result = ladder
        for rnd in ladder.rounds:
            self.ledger.append(
                "ladder_round",
                {
                    "round": rnd.round_index,
                    "bit": rnd.bit,
                    "nodes": len(rnd.nodes),
                    "merkle_root": rnd.root,
                    "holds": rnd.holds,
                    "repairs": rnd.repairs,
                    "words": [n.word for n in rnd.nodes],
                },
            )
            for n in rnd.nodes:
                if n.commit_status == "held":
                    self.ledger.append(
                        "vdr_hint",
                        {
                            "node": n.name,
                            "action": "swap_pairing",
                            "detail": f"pair fusion held ({n.commit_reason}); "
                                      f"round retried on alternate bits",
                        },
                    )
        assert ladder.root_node is not None
        root = ladder.root_node

        recon = self._reconcile(root.module)
        self.ledger.append("reconciliation", recon)
        if recon["decision"] != "adopt":
            self.ledger.append(
                "vdr_hint",
                {
                    "action": "reconciliation_hold",
                    "detail": (
                        "meta/aggregate council did not adopt: "
                        f"gamma_delta={recon['gamma_delta']}, "
                        f"committed={recon['committed_count']} "
                        f"< quorum={recon['quorum']}"
                        if recon["committed_count"] < recon["quorum"]
                        else f"gamma_delta={recon['gamma_delta']} above tau"
                    ),
                },
            )
            return None

        key = session_key(self.prompt, self.session_id)
        leaf_root = merkle_root(self._leaf_hashes_list())
        stamp = decision_stamp(
            key=key,
            leaf_root=leaf_root,
            round_roots=ladder.round_roots,
            decision_coordinate=recon["coordinate"]["dyadic"],
            head_hash=self.ledger.head_hash,
        )
        stamp_payload = {
            "leaf_root": leaf_root,
            "round_roots": ladder.round_roots,
            "coordinate": recon["coordinate"],
            "head_at_stamp": self.ledger.head_hash,
            "challenge": gate_challenge(key),
            "stamp": stamp,
        }
        self.ledger.append("decision_stamp", stamp_payload)

        top = sorted(
            (
                (i, s)
                for i, s in self.slots.items()
                if s.metrics is not None and any(t != 0 for t in s.last_word)
            ),
            key=lambda kv: kv[1].metrics.coverage * kv[1].metrics.coherence,  # type: ignore[union-attr]
            reverse=True,
        )[:8]
        release = {
            "session_id": self.session_id,
            "prompt": self.prompt,
            "cycle": self.cycle,
            "tier": report.headline_tier,
            "tier_histogram": report.tier_histogram,
            "root_word": root.word,
            "root_tier": root.tier,
            "coordinate": recon["coordinate"],
            "global_S": _r(self.S_history[-1]) if self.S_history else 0.0,
            "gate": report.to_json(),
            "stamp": stamp,
            "leaf_root": leaf_root,
            "budget_release": report.budget_release,
            "top_slots": [
                {
                    "slot": i,
                    "address": list(address_of_index(i)),
                    "axes": {
                        self.config.axes[k]: address_of_index(i)[k]
                        for k in range(3)
                    },
                    "word": to_word(s.last_word),
                    "tier": classify(s.last_word),
                    "metrics": s.metrics.to_json() if s.metrics else None,
                }
                for i, s in top
            ],
        }
        self.ledger.append("release", release)
        self.release_record = release
        return release

    def _reconcile(self, root_module: Module) -> dict[str, Any]:
        """The final dyad: Meta_Imagination <-> Aggregate_Internal as a council."""
        c = self.config

        # Aggregate_Internal: per-position superposition over all leaf write cones
        agg_read = []
        for pos in range(3):
            acc = 0j
            n = 0
            for i in range(64):
                vals = self.field.modules[self._slot_name(i)].write_values()
                if abs(vals[pos]) > 0:
                    acc = interfere(acc, vals[pos])
                    n += 1
            agg_read.append(acc / n if n else 0j)
        agg_dyad = corefold_3_to_2(agg_read)
        agg_sing = corefold_2_to_1(agg_dyad)
        aggregate = Module(
            name="aggregate",
            cells=[Cell(theta=phase(v), amp=abs(v)) for v in agg_read]
            + [
                Cell(theta=phase(agg_dyad[0]), amp=abs(agg_dyad[0])),
                Cell(theta=phase(agg_sing), amp=abs(agg_sing)),
                Cell(theta=phase(agg_dyad[1]), amp=abs(agg_dyad[1])),
            ],
            belief=root_module.belief,
            prior=root_module.prior,
        )

        # Meta_Imagination: the root's synthesis under action-mode prior
        # pressure (the action half of the dual minimizer: output phase moves
        # so evidence shifts toward the prior - extrapolative but grounded).
        # The pull scales with |prior|: an uninformed prior (≈0) exerts no
        # pressure (E0: intent frames need prior *pressure*, and none exists).
        prior_mag = min(1.0, abs(root_module.prior))
        prior_theta = polarity_to_theta(max(-1.0, min(1.0, root_module.prior)))
        base = []
        for v in root_module.write_values():
            th = phase(v)
            th = wrap_angle(
                th
                + root_module.action_gain * 0.5 * prior_mag
                * wrap_angle(prior_theta - th)
            )
            base.append(coh(abs(v), th))
        m_dyad = corefold_3_to_2(base)
        m_sing = corefold_2_to_1(m_dyad)
        meta = Module(
            name="meta",
            cells=[Cell(theta=phase(v), amp=abs(v)) for v in base]
            + [
                Cell(theta=phase(m_dyad[0]), amp=abs(m_dyad[0])),
                Cell(theta=phase(m_sing), amp=abs(m_sing)),
                Cell(theta=phase(m_dyad[1]), amp=abs(m_dyad[1])),
            ],
            belief=root_module.belief,
            prior=root_module.prior,
        )

        # The reconciliation dyad is a *committing measurement*: its commit
        # must not increase Φ (trace/window witness), so the council field
        # runs snap-free - pure quantize + belief + latch. Cross-member
        # channels give the read cones live afferents, and snapping against
        # a live afferent is what costs orientation energy.
        council = Field(
            name="council",
            dt=c.dt,
            gain=c.gain,
            deadband=c.deadband,
            snap=0.0,
            belief_gain=c.belief_gain,
            amp_relax=c.amp_relax,
        )
        council.add_module(meta)
        council.add_module(aggregate)
        # bidiγΔ: two α=0 module-level relations, both directions
        council.add_channel(Channel(src="meta", dst="aggregate",
                                    weight=c.recon_weight))
        council.add_channel(Channel(src="aggregate", dst="meta",
                                    weight=c.recon_weight))
        council.flow(c.recon_flow)
        meta_commit = council.commit("meta")
        agg_commit = council.commit("aggregate")

        meta_word = tuple(
            meta_commit.trits[i] for i in council.modules["meta"].write_cone
        )
        agg_word = tuple(
            agg_commit.trits[i] for i in council.modules["aggregate"].write_cone
        )
        member_trits = meta_word + agg_word
        row: BridgeRow = project_trits(member_trits)
        committed_count = sum(1 for t in member_trits if t != 0)
        g_delta = abs(
            coherence_delta(
                council.modules["meta"].cells[4].value(),
                council.modules["aggregate"].cells[4].value(),
            )
        )
        adopted = (
            meta_commit.status == "accepted"
            and agg_commit.status == "accepted"
            and committed_count >= c.recon_quorum
            and g_delta <= c.tau_recon
        )
        return {
            "meta_word": to_word(meta_word),
            "aggregate_word": to_word(agg_word),
            "meta_status": f"{meta_commit.status}:{meta_commit.reason}",
            "aggregate_status": f"{agg_commit.status}:{agg_commit.reason}",
            "gamma_delta": _r(g_delta),
            "tau_recon": c.tau_recon,
            "committed_count": committed_count,
            "quorum": c.recon_quorum,
            "decision": "adopt" if adopted else "hold",
            "coordinate": {
                "dyadic": row.dyadic,
                "triadic": row.triadic,
                "index": row.index,
            },
        }

    # ------------------------------------------------------------------ #
    # observation surface (passive; for hosts and frontends)
    # ------------------------------------------------------------------ #

    def viability(self) -> dict[str, Any]:
        """E0 existence-viability report: mode + transition capacity."""
        open_slots = [
            i for i, s in self.slots.items()
            if s.atom_count > 0 and not s.saturated
        ]
        capacity = bool(
            self.pending
            or self.intents
            or (open_slots and self.release_record is None)
        )
        if self.release_record is not None:
            mode = "passive"        # persists as a replayable value
        elif self.intents:
            mode = "agentic"        # asking its environment for evidence
        elif self.pending or open_slots:
            mode = "reactive"
        else:
            mode = "intentional"    # priors set, awaiting relation
        return {
            "mode": mode,
            "viable": True,
            "transition_capacity": capacity,
            "pending_atoms": len(self.pending),
            "open_intents": len(self.intents),
            "open_slots": open_slots,
            "budget_remaining": self.config.retrieval_budget - self.intents_emitted,
            "released": self.release_record is not None,
        }

    def state_json(self) -> dict[str, Any]:
        """Full board projection (the frontend coupling surface)."""
        board = []
        for i in range(64):
            s = self.slots[i]
            q = address_of_index(i)
            board.append(
                {
                    "slot": i,
                    "dyadic": dyadic_of_index(i),
                    "triadic": "".join(str(x) for x in q),
                    "axes": {self.config.axes[k]: q[k] for k in range(3)},
                    "atoms": s.atom_count,
                    "absorbed": _r(s.absorbed),
                    "word": to_word(s.last_word),
                    "tier": classify(s.last_word),
                    "saturated": s.saturated,
                    "open_intent": s.open_intent,
                    "metrics": s.metrics.to_json() if s.metrics else None,
                }
            )
        return {
            "engine": "gist-engine",
            "version": _pkg_version,
            "session_id": self.session_id,
            "prompt": self.prompt,
            "cycle": self.cycle,
            "axes": list(self.config.axes),
            "S": _r(self.S_history[-1]) if self.S_history else 0.0,
            "S_history": [_r(x) for x in self.S_history[-16:]],
            "board": board,
            "gate": self.gate_report.to_json() if self.gate_report else None,
            "intents": [
                {
                    "intent_id": it.intent_id,
                    "slot": it.slot,
                    "address": list(it.address),
                    "openness": _r(it.openness),
                    "query_hint": it.query_hint,
                }
                for it in self.intents.values()
            ],
            "viability": self.viability(),
            "ladder": self.ladder_result.to_json() if self.ladder_result else None,
            "release": self.release_record,
            "ledger_head": self.ledger.head_hash,
            "ledger_length": len(self.ledger),
        }

    def export_replay(self) -> dict[str, Any]:
        """Frontend replay bundle (the CDC demo/replay.json pattern)."""
        return {
            "engine": "gist-engine",
            "version": _pkg_version,
            "session_id": self.session_id,
            "prompt": self.prompt,
            "events": [e.to_json() for e in self.ledger],
            "final_state": self.state_json(),
        }


# ---------------------------------------------------------------------- #
# third-party replay verification
# ---------------------------------------------------------------------- #

SEMANTIC_KINDS = (
    "session_init",
    "atom_queued",
    "cycle_start",
    "atom_ingested",
    "slot_commit",
    "slot_metrics",
    "slot_saturated",
    "retrieval_intent",
    "escalation_intent",
    "intent_fulfilled",
    "vdr_hint",
    "gate_eval",
    "gate_proposal",
    "ladder_round",
    "reconciliation",
    "decision_stamp",
    "release",
    "cycle_end",
)

# input events feed a replay; all other kinds are derived and regenerated
INPUT_KINDS = ("session_init", "atom_queued", "intent_fulfilled", "cycle_start")


class LedgerReplayError(Exception):
    pass


def replay_engine(recorded: Ledger) -> GistEngine:
    """Rebuild a live engine by feeding only the recorded input events.

    session_init seeds the engine; atom_queued events re-queue their recorded
    projected geometry (no projector needed); intent_fulfilled events reapply
    the host's bookkeeping; each cycle_start marker re-runs one step(). All
    derived events (commits, metrics, gate, ladder, stamp, release) are
    regenerated by the deterministic engine.
    """
    init = recorded.last_of_kind("session_init")
    if init is None:
        raise LedgerReplayError("no session_init in ledger")
    engine = GistEngine(
        prompt=init.payload["prompt"],
        session_id=init.payload["session_id"],
        config=GistConfig.from_json(init.payload["config"]),
        _replaying=True,
    )
    engine.ledger.append("session_init", init.payload)
    for e in recorded:
        if e.kind == "atom_queued":
            p = e.payload
            engine.pending.append(
                (
                    ProjectedAtom(
                        content=p["content"],
                        slot=p["slot"],
                        polarity=p["polarity"],
                        salience=p["salience"],
                        theta=p["theta"],
                        amplitude=p["amplitude"],
                        provenance=p.get("provenance", {}),
                    ),
                    p["source"],
                )
            )
            engine.ledger.append("atom_queued", p)
        elif e.kind == "intent_fulfilled":
            f = e.payload
            slot = engine.slots[f["slot"]]
            slot.fulfillments += 1
            slot.open_intent = None
            slot.saturated = False
            slot.coherence_history.clear()
            slot.last_statuses.clear()
            engine.intents.pop(f["intent_id"], None)
            engine.ledger.append("intent_fulfilled", f)
        elif e.kind == "cycle_start":
            engine.step()
    return engine


def verify_ledger(path: str | Path) -> dict[str, Any]:
    """Replay a session ledger from inputs alone and compare every derived event.

    Returns {verified, chain_ok, events, mismatches[...]}. `verified` is True
    iff the hash chain holds AND a fresh engine, fed only the recorded inputs
    (queued projected atoms, fulfillments, cycle markers, config, prompt),
    reproduces the identical payload stream - commits, metrics, gate reports,
    Merkle roots, reconciliation, and stamp included.
    """
    from .ledger import LedgerError

    try:
        recorded = Ledger.load(path)
    except LedgerError as err:
        return {"verified": False, "chain_ok": False, "error": str(err),
                "events": 0, "mismatches": [{"detail": "hash chain broken"}]}
    chain_ok = recorded.verify_chain()

    try:
        engine = replay_engine(recorded)
    except LedgerReplayError as err:
        return {"verified": False, "chain_ok": chain_ok,
                "error": str(err), "events": len(recorded)}

    mismatches: list[dict[str, Any]] = []
    rec_stream = [
        (e.kind, e.payload) for e in recorded if e.kind in SEMANTIC_KINDS
    ]
    new_stream = [
        (e.kind, e.payload) for e in engine.ledger if e.kind in SEMANTIC_KINDS
    ]
    for idx, (a, b) in enumerate(zip(rec_stream, new_stream)):
        if a != b:
            mismatches.append(
                {"index": idx, "recorded": {"kind": a[0]},
                 "replayed": {"kind": b[0]},
                 "detail": _first_diff(a[1], b[1]) if a[0] == b[0]
                 else f"kind {a[0]} != {b[0]}"}
            )
            if len(mismatches) >= 8:
                break
    if len(rec_stream) != len(new_stream):
        mismatches.append(
            {"detail": f"stream length {len(rec_stream)} != {len(new_stream)}"}
        )

    return {
        "verified": chain_ok and not mismatches,
        "chain_ok": chain_ok,
        "events": len(recorded),
        "replayed_events": len(engine.ledger),
        "mismatches": mismatches,
        "head_recorded": recorded.head_hash,
        "head_replayed": engine.ledger.head_hash,
    }


def _first_diff(a: dict[str, Any], b: dict[str, Any]) -> str:
    sa, sb = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)
    for i, (x, y) in enumerate(zip(sa, sb)):
        if x != y:
            lo = max(0, i - 40)
            return f"...{sa[lo:i + 40]}... != ...{sb[lo:i + 40]}..."
    return f"length {len(sa)} != {len(sb)}"
