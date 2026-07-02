"""Fields, modules, cells, channels, and the hybrid reduction relation.

This module implements the CDC semantic kernel that GIST is built out of:

  flow(d)    continuous reduction: phase turns toward the afferent
             superposition, amplitude relaxes, belief descends prediction
             error (exact gradient of the potential's belief terms).
  commit(m)  guarded discrete reduction: snap -> barrier -> belief -> guard
             -> latch, total (accepted or held, never partial), with the
             explicit statuses and reasons of the CDC native runtime:
             accepted / held + none / balance-violation / energy-increase /
             deadband-jitter.
  nest(p,c)  bidiγΔ at α=0: child coherence flows up into the parent belief,
             parent context flows down into the child prior.

Parity: the numeric semantics reproduce the executable witnesses declared in
the CDC repository's `native_reducer.cdc`:

  flow    channel a->b weight 0.25, θ_a=π/2, θ_b=0, duration 1.0 (frozen
          afferent) => θ_b = 0.25 exactly.
  commit  cells at θ = (π/2, 0, π) => trits '0+-', admissible, accepted/none.
  hold    cells at θ = (π, 0, π/2) => candidate '-+0', prefix walk hits -1,
          held/balance-violation, no state mutation.
  nest    parent belief <- mean κ(child cells) = 2/3, then child prior <-
          parent belief = 2/3.

Where the prose spec and the executable native witnesses diverge (the core
document describes rotating barrier violators to their crossing inside the
commit; the native runtime *holds* the commit with reason balance-violation),
this engine follows the executable witness by default (`barrier='hold'`) and
offers the prose semantics as `barrier='repair'`. GIST drives repair through
visible VDR hints in the ledger rather than silent in-commit mutation.

The potential (variational free energy) per module:

  Φ_m = Σ_i [ ½·π·(Re Â_i − b)²  +  ½·(b − b⁰)²  −  |Â_i|·cos(arg Â_i − θ_i) ]

with π the module precision, b its belief, b⁰ its prior. Accepted commits
never increase Φ_m (metatheorem T2, Soundness); candidate words that would go
into coherence debt are held (metatheorem T1, Preservation).
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, field as dc_field
from typing import Iterable

from .algebra import (
    Coh,
    VOID,
    amplitude,
    coh,
    interfere,
    kappa,
    phase,
    rotate,
    trit,
    wrap_angle,
)
from .walks import first_violation, is_admissible, to_word

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


@dataclass
class Cell:
    """A phase-state carrier: continuous phase + amplitude, latched pole."""

    theta: float = 0.0
    amp: float = 1.0
    omega: float = 0.0        # intrinsic angular velocity
    plasticity: float = 0.0
    sigma: int = 0            # latched committed pole (balanced trit)
    memory: float = 0.0

    def value(self) -> Coh:
        return coh(self.amp, self.theta)

    def copy(self) -> "Cell":
        return Cell(self.theta, self.amp, self.omega,
                    self.plasticity, self.sigma, self.memory)


@dataclass
class Channel:
    """A directed influence: weight × delay × angular bias × line projection.

    Paths address a module (`"m"`, meaning its cells broadcast/aggregate) or
    a single cell (`"m:i"`). `lines` restricts which destination cell indices
    receive the influence (None = all destination lines).
    """

    src: str
    dst: str
    weight: float = 1.0
    delay: float = 0.0
    angle: float = 0.0
    lines: tuple[int, ...] | None = None
    plastic: bool = False


@dataclass
class Module:
    """A bounded boundary: n cells with read/write cones, belief, prior."""

    name: str
    cells: list[Cell]
    belief: float = 0.0
    prior: float = 0.0
    precision: float = 1.0
    action_gain: float = 1.0
    parent: str | None = None
    # canonical n=6 cones; smaller modules default to all-cells cones
    read_cone: tuple[int, ...] = ()
    write_cone: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        n = len(self.cells)
        if not self.read_cone and not self.write_cone:
            if n == 6:
                self.read_cone = (0, 1, 2)
                self.write_cone = (3, 4, 5)
            else:
                self.read_cone = tuple(range(n))
                self.write_cone = tuple(range(n))

    def cell_values(self) -> list[Coh]:
        return [c.value() for c in self.cells]

    def read_values(self) -> list[Coh]:
        return [self.cells[i].value() for i in self.read_cone]

    def write_values(self) -> list[Coh]:
        return [self.cells[i].value() for i in self.write_cone]

    def trits(self, deadband: float) -> tuple[int, ...]:
        return tuple(trit(c.value(), deadband) for c in self.cells)

    def latched_word(self) -> tuple[int, ...]:
        return tuple(c.sigma for c in self.cells)

    def copy(self) -> "Module":
        m = Module(
            name=self.name,
            cells=[c.copy() for c in self.cells],
            belief=self.belief,
            prior=self.prior,
            precision=self.precision,
            action_gain=self.action_gain,
            parent=self.parent,
            read_cone=self.read_cone,
            write_cone=self.write_cone,
        )
        return m


@dataclass
class CommitResult:
    module: str
    status: str                 # 'accepted' | 'held'
    reason: str                 # 'none' | 'balance-violation' | 'energy-increase'
                                # | 'deadband-jitter'
    trits: tuple[int, ...]      # candidate word (latched only if accepted)
    word: str
    admissible: bool
    phi_before: float
    phi_after: float
    violation_cell: int | None = None
    repaired_cells: tuple[int, ...] = ()

    @property
    def accepted(self) -> bool:
        return self.status == "accepted"


# ---------------------------------------------------------------------------
# Field
# ---------------------------------------------------------------------------


@dataclass
class Field:
    """A graph of modules and channels under the hybrid reduction relation."""

    name: str = "field"
    dt: float = 0.125
    gain: float = 1.0
    deadband: float = 0.5
    snap: float = 0.5             # commit snap fraction toward the pole
    belief_gain: float = 0.5      # commit-time belief step toward evidence
    amp_relax: float = 0.0        # flow amplitude relaxation rate (0 = off)
    energy_tolerance: float = 1e-9
    time: float = 0.0
    modules: dict[str, Module] = dc_field(default_factory=dict)
    channels: list[Channel] = dc_field(default_factory=list)

    # -- construction ------------------------------------------------------

    def add_module(self, module: Module) -> Module:
        if module.name in self.modules:
            raise ValueError(f"duplicate module {module.name!r}")
        self.modules[module.name] = module
        return module

    def add_channel(self, channel: Channel) -> Channel:
        self.channels.append(channel)
        return channel

    # -- addressing --------------------------------------------------------

    def _resolve_src(self, path: str) -> Coh:
        """Source value of a path: a single cell, or a module's write latent."""
        if ":" in path:
            mod, idx = path.split(":")
            return self.modules[mod].cells[int(idx)].value()
        m = self.modules[path]
        # module-level source: superposition mean of its write cone
        vals = m.write_values()
        return interfere(*vals) / len(vals) if vals else VOID

    def _dst_cells(self, path: str, lines: tuple[int, ...] | None) -> list[tuple[Module, int]]:
        if ":" in path:
            mod, idx = path.split(":")
            return [(self.modules[mod], int(idx))]
        m = self.modules[path]
        targets = lines if lines is not None else m.read_cone
        return [(m, i) for i in targets]

    # -- afferents ---------------------------------------------------------

    def afferents(self, module: Module) -> list[Coh]:
        """Per-cell afferent superposition Â for a module.

        Each incident channel contributes weight · ⟳_angle(source value).
        (Openness gating is a documented divergence: the CDC prose gates
        afferents by boundary openness, but the executable native witnesses
        do not; this engine follows the executable witnesses.)
        """
        aff: list[Coh] = [VOID for _ in module.cells]
        for ch in self.channels:
            dst_mod = ch.dst.split(":")[0]
            if dst_mod != module.name:
                continue
            src_val = self._resolve_src(ch.src)
            contrib = rotate(ch.angle, src_val) * ch.weight
            for m, i in self._dst_cells(ch.dst, ch.lines):
                if m.name == module.name and 0 <= i < len(aff):
                    aff[i] = interfere(aff[i], contrib)
        return aff

    # -- potential ---------------------------------------------------------

    def phi(self, module: Module, afferents: list[Coh] | None = None) -> float:
        """Variational free energy Φ_m (see module docstring)."""
        aff = afferents if afferents is not None else self.afferents(module)
        b = module.belief
        b0 = module.prior
        pi = module.precision
        total = 0.0
        for cell, a in zip(module.cells, aff):
            re_a = a.real
            total += 0.5 * pi * (re_a - b) ** 2
            total += 0.5 * (b - b0) ** 2
            amp_a = amplitude(a)
            if amp_a > 0.0:
                total -= amp_a * math.cos(phase(a) - cell.theta)
        return total

    def phi_total(self) -> float:
        return sum(self.phi(m) for m in self.modules.values())

    # -- flow ⟶_d ----------------------------------------------------------

    def flow(self, duration: float, frozen: bool = False) -> None:
        """Continuous reduction for `duration`.

        frozen=True evaluates afferents once and applies a single linear step
        of the full duration (the realization used by the CDC native runtime's
        flow jobs, and the one its parity witnesses pin). frozen=False
        integrates with explicit Euler steps of size dt (the engine's richer
        realization; T4 additivity holds for the underlying relation, and the
        integrator choice is a recorded realization parameter, not calculus).
        """
        if duration <= 0.0:
            return
        if frozen:
            self._flow_step(duration)
            self.time += duration
            return
        remaining = duration
        while remaining > 1e-12:
            step = min(self.dt, remaining)
            self._flow_step(step)
            remaining -= step
        self.time += duration

    def _flow_step(self, step: float) -> None:
        # evaluate all afferents against the pre-step state (synchronous step)
        plans: list[tuple[Module, list[Coh]]] = []
        for m in self.modules.values():
            plans.append((m, self.afferents(m)))
        for m, aff in plans:
            # cells: phase turns toward the incoming superposition
            for cell, a in zip(m.cells, aff):
                dtheta = cell.omega
                amp_a = amplitude(a)
                if amp_a > 0.0:
                    dtheta += self.gain * amp_a * math.sin(phase(a) - cell.theta)
                cell.theta = wrap_angle(cell.theta + step * dtheta)
                if self.amp_relax > 0.0 and amp_a > 0.0:
                    cell.amp += step * self.amp_relax * (amp_a - cell.amp)
                    cell.amp = max(0.0, cell.amp)
            # belief: exact gradient descent of Φ's belief terms
            if m.cells:
                mean_re = sum(a.real for a in aff) / len(aff)
                db = m.precision * (mean_re - m.belief) - (m.belief - m.prior)
                m.belief += step * db
        # plastic channels: weights follow correlation (Hebbian, bounded)
        for ch in self.channels:
            if not ch.plastic:
                continue
            src_val = self._resolve_src(ch.src)
            for m, i in self._dst_cells(ch.dst, ch.lines):
                dst_val = m.cells[i].value()
                corr = (
                    amplitude(src_val)
                    * amplitude(dst_val)
                    * math.cos(phase(src_val) - phase(dst_val))
                )
                ch.weight += step * m.cells[i].plasticity * (corr - ch.weight)

    # -- commit ⟶_β --------------------------------------------------------

    def commit(self, name: str, barrier: str = "hold") -> CommitResult:
        """Guarded discrete reduction of one module. Total: accepts or holds.

        Steps (atomic; computed on a candidate copy, applied only on accept):
          1. quantize + snap: the candidate word is the balanced-ternary
                     quantization of the *current* state (the trit is the
                     commitment); each decisively polarized READ-CONE cell
                     then snaps a fraction toward the pole its trit selects
                     (the evidence triad hardens), while crossing cells stay
                     at their crossing (their openness is real) and write-
                     cone cells stay flow-aligned. Because afferents Â are
                     frozen at commit time and read cells carry no incident
                     afferent, the read-cone snap is exactly Φ-neutral: the
                     energy guard then judges only the belief step, which
                     makes commits event-driven - they accept on fresh
                     evidence and hold (deadband-jitter) at plateau;
          2. barrier prefix trit walk must stay nonnegative, else hold with
                     balance-violation (or, in 'repair' mode, rotate the
                     violating cells to their crossing and re-walk);
          3. jitter  a candidate word identical to the already-latched word
                     is held as deadband-jitter (the plateau signal);
          4. belief  step toward the evidence mean Re Â;
          5. guard   if Φ_m would increase, hold with energy-increase;
          6. latch   write poles σ, apply candidate state, accept.
        """
        m = self.modules[name]
        aff = self.afferents(m)
        phi_before = self.phi(m, aff)

        # -- 1. quantize, then snap the read cone toward committed poles
        cand_trits = m.trits(self.deadband)
        candidate = m.copy()
        if self.snap > 0.0:
            read = set(m.read_cone)
            for i, (cell, t) in enumerate(zip(candidate.cells, cand_trits)):
                if t == 0 or i not in read:
                    continue  # crossings stay open; write cone stays fluid
                p = 0.0 if t > 0 else math.pi
                cell.theta = wrap_angle(
                    cell.theta + self.snap * wrap_angle(p - cell.theta)
                )

        repaired: list[int] = []

        # -- 2. barrier (T1 Preservation)
        if not is_admissible(cand_trits):
            violation = first_violation(cand_trits)
            if barrier == "repair":
                # prose-spec semantics: rotate debt-forcing cells to crossing
                trits_list = list(cand_trits)
                while not is_admissible(trits_list):
                    idx = first_violation(trits_list)
                    assert idx is not None
                    cell = candidate.cells[idx]
                    # nearest crossing: ±π/2, preserving the sin sign
                    cell.theta = (
                        math.copysign(math.pi / 2.0, math.sin(cell.theta))
                        if math.sin(cell.theta) != 0.0
                        else math.pi / 2.0
                    )
                    trits_list[idx] = 0
                    repaired.append(idx)
                cand_trits = tuple(trits_list)
            else:
                return CommitResult(
                    module=name,
                    status="held",
                    reason="balance-violation",
                    trits=cand_trits,
                    word=to_word(cand_trits),
                    admissible=False,
                    phi_before=phi_before,
                    phi_after=phi_before,
                    violation_cell=violation,
                )

        # -- 3. deadband-jitter (plateau: nothing new to commit)
        # Holds when the candidate word repeats the latch, or when there is
        # nothing decisive to latch at all (an all-crossing word): no new
        # commitment content crossed the deadband.
        if cand_trits == m.latched_word() and (
            any(c.sigma != 0 for c in m.cells)
            or all(t == 0 for t in cand_trits)
        ):
            return CommitResult(
                module=name,
                status="held",
                reason="deadband-jitter",
                trits=cand_trits,
                word=to_word(cand_trits),
                admissible=True,
                phi_before=phi_before,
                phi_after=phi_before,
            )

        # -- 4. belief step toward the evidence (perception)
        # The step targets the Φ-minimizing precision-weighted blend of
        # evidence and prior, b* = (π·mean(Re Â) + b⁰) / (π + 1): the exact
        # discrete counterpart of the belief flow's gradient descent, so the
        # step never raises the belief terms of Φ (T2 by construction).
        if candidate.cells:
            mean_re = sum(a.real for a in aff) / len(aff)
            b_star = (
                (candidate.precision * mean_re + candidate.prior)
                / (candidate.precision + 1.0)
            )
            candidate.belief += self.belief_gain * (b_star - candidate.belief)

        # -- 5. guard (T2 Soundness): hold on potential increase
        phi_after = self.phi(candidate, aff)
        if phi_after > phi_before + self.energy_tolerance:
            return CommitResult(
                module=name,
                status="held",
                reason="energy-increase",
                trits=cand_trits,
                word=to_word(cand_trits),
                admissible=True,
                phi_before=phi_before,
                phi_after=phi_after,
            )

        # -- 6. latch and apply
        for cell, t in zip(candidate.cells, cand_trits):
            cell.sigma = t
        self.modules[name] = candidate
        return CommitResult(
            module=name,
            status="accepted",
            reason="none",
            trits=cand_trits,
            word=to_word(cand_trits),
            admissible=True,
            phi_before=phi_before,
            phi_after=phi_after,
            repaired_cells=tuple(repaired),
        )

    # -- do (graph surgery: the interventional twin) --------------------------

    def do(self, assignments: dict[str, int]) -> "Field":
        """Pearl's mutilated-graph operator on the field: a pure twin.

        For each module m in `assignments` with pole t ∈ {-1, 0, +1}:
        sever every channel inbound to m (delete the structural equation)
        and pin every cell of m at the pole for t (θ = 0 for +1, π for -1,
        π/2 for 0; σ latched). With no afferents and ω = 0 the pinned
        module is a fixed point of flow: the intervention holds without
        any additional freezing machinery. The original field is untouched.
        """
        pole_theta = {1: 0.0, -1: math.pi, 0: math.pi / 2.0}
        for name, t in assignments.items():
            if name not in self.modules:
                raise KeyError(f"unknown module {name!r}")
            if t not in pole_theta:
                raise ValueError(f"pole must be a balanced trit, got {t!r}")
        twin = Field(
            name=f"{self.name}::do",
            dt=self.dt,
            gain=self.gain,
            deadband=self.deadband,
            snap=self.snap,
            belief_gain=self.belief_gain,
            amp_relax=self.amp_relax,
            energy_tolerance=self.energy_tolerance,
        )
        for name, m in self.modules.items():
            twin.add_module(m.copy())
        for ch in self.channels:
            dst_mod = ch.dst.split(":")[0]
            if dst_mod in assignments:
                continue  # severed: the intervened module obeys only do()
            twin.channels.append(Channel(
                src=ch.src, dst=ch.dst, weight=ch.weight, delay=ch.delay,
                angle=ch.angle, lines=ch.lines, plastic=ch.plastic,
            ))
        for name, t in assignments.items():
            for cell in twin.modules[name].cells:
                cell.theta = pole_theta[t]
                cell.omega = 0.0
                cell.sigma = t
                if cell.amp == 0.0:
                    cell.amp = 1.0
        return twin

    # -- nest (bidiγΔ at α = 0) ---------------------------------------------

    def nest(self, parent: str, child: str, gain: float = 1.0) -> tuple[float, float]:
        """Cross-scale exchange: child coherence up, parent context down.

        up:   parent.belief += gain · (mean κ(child cells) − parent.belief)
        down: child.prior   += gain · (parent.belief − child.prior)

        With gain=1 this reproduces the CDC native witness numbers
        (parent belief = child prior = 2/3 for the declared scenario).
        Returns (parent_belief, child_prior) after the exchange.
        """
        p = self.modules[parent]
        c = self.modules[child]
        if c.cells:
            child_coherence = sum(kappa(cell.value()) for cell in c.cells) / len(c.cells)
        else:
            child_coherence = 0.0
        p.belief += gain * (child_coherence - p.belief)
        c.prior += gain * (p.belief - c.prior)
        return (p.belief, c.prior)

    # -- observation (derived; passive) -------------------------------------

    def trace_trits(self, module_names: Iterable[str] | None = None) -> tuple[int, ...]:
        """Passive trace: concatenated current trits of the named modules.

        Pure read - does not alter phase, belief, commits, or potential
        (trace/window witness: passive observation leaves state unchanged).
        """
        names = list(module_names) if module_names is not None else list(self.modules)
        out: list[int] = []
        for n in names:
            out.extend(self.modules[n].trits(self.deadband))
        return tuple(out)
