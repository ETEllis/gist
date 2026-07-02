"""Slot and field metrics: every GIST score computed from calculus state.

No metric here is asserted or estimated by a model; each is a deterministic
function of field geometry, so replay always reproduces it exactly.

  coherence   phase-order magnitude of the slot's write cone (CDC's
              phase-order magnitude; the Kuramoto mean resultant length).

  coverage c  1 - exp(-A / lambda): saturating function of the cumulative
              afferent amplitude A the slot has absorbed. Amplitude is the
              calculus's evidence-mass carrier, so coverage is literally
              "how much evidence mass reached this scope".

  stability u fraction of a fixed set of deterministic phase perturbations
              (sign-patterned jitters) under which the slot re-quantizes to
              the same committed word. Robustness under ablation, executed
              as actual perturbed re-quantization - not a guess.

  cf agreement a  counterfactual survival, Pearl-style but executed on the
              calculus's own causal fabric: for each read cell, build the
              twin module (the twin network), intervene do(cell := pole
              flip) with the intervened cell latched, re-flow the intra-slot
              channel graph, re-quantize, and check whether the singular
              conclusion (write-cone trit word) survives. a = survival
              fraction over interventions. This measures evidential
              triangulation: a conclusion carried by redundant, phase-
              diverse evidence survives interventions; a knife-edge or
              contested conclusion does not. Structural ceiling (documented,
              by construction): a slot whose conclusion is carried by one
              dominant evidence cluster tops out at (n_read - 1) / n_read =
              2/3, because flipping the dominant cluster must flip an honest
              synthesis; scores below that indicate knife-edge amplitude
              balances or contested evidence. A semantic CF validator can be
              layered on top through the ports; this structural one is the
              mechanism's own, and it is exact.

  causal lift ell  normalized free-energy drop attributable to the evidence:
              (Phi_vacuum - Phi_actual) / (1 + |Phi_vacuum|), clamped to
              [0, 1], where the vacuum twin has all afferents removed. High
              lift = the evidence structure genuinely lowers the slot's
              variational free energy relative to prior-only existence.

  global S    amplitude-weighted phase-order magnitude over all slots'
              singular cells - the field-level agreement GIST gates on.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .algebra import phase_order, openness as cell_openness, wrap_angle
from .field import Field, Module

COVERAGE_LAMBDA = 3.0

# 8 fixed sign patterns over 6 cells (rows of a deterministic +-1 table).
_JITTER_PATTERNS: tuple[tuple[int, ...], ...] = (
    (+1, +1, +1, +1, +1, +1),
    (-1, -1, -1, -1, -1, -1),
    (+1, -1, +1, -1, +1, -1),
    (-1, +1, -1, +1, -1, +1),
    (+1, +1, -1, -1, +1, +1),
    (-1, -1, +1, +1, -1, -1),
    (+1, -1, -1, +1, -1, +1),
    (-1, +1, +1, -1, +1, -1),
)
JITTER_ANGLE = 0.15  # radians; a realization parameter, recorded in config


def slot_coherence(module: Module) -> float:
    """Phase-order magnitude of the write cone."""
    return phase_order(module.write_values())


def slot_openness(module: Module, deadband: float) -> float:
    """Mean boundary openness of the read cone (aperture to new relation)."""
    vals = module.read_values()
    if not vals:
        return 1.0
    return sum(cell_openness(v, deadband) for v in vals) / len(vals)


def coverage(absorbed_amplitude: float, lam: float = COVERAGE_LAMBDA) -> float:
    """c = 1 - exp(-A/lambda), monotone saturating in evidence mass."""
    return 1.0 - math.exp(-max(0.0, absorbed_amplitude) / lam)


def stability(field: Field, name: str, jitter: float = JITTER_ANGLE) -> float:
    """u: survival fraction of the committed word under fixed phase jitters."""
    module = field.modules[name]
    committed = module.latched_word()
    if all(t == 0 for t in committed):
        committed = module.trits(field.deadband)
    n = len(module.cells)
    survived = 0
    for pattern in _JITTER_PATTERNS:
        twin = module.copy()
        for i, cell in enumerate(twin.cells):
            cell.theta = wrap_angle(cell.theta + jitter * pattern[i % len(pattern)])
        if twin.trits(field.deadband) == committed:
            survived += 1
    return survived / len(_JITTER_PATTERNS) if n else 0.0


def _twin_field_single(field: Field, name: str) -> Field:
    """A twin field containing a copy of one module and its intra-module channels."""
    twin = Field(
        name=f"{field.name}::twin",
        dt=field.dt,
        gain=field.gain,
        deadband=field.deadband,
        snap=field.snap,
        belief_gain=field.belief_gain,
        amp_relax=field.amp_relax,
    )
    twin.add_module(field.modules[name].copy())
    for ch in field.channels:
        src_mod = ch.src.split(":")[0]
        dst_mod = ch.dst.split(":")[0]
        if src_mod == name and dst_mod == name:
            twin.channels.append(
                type(ch)(src=ch.src, dst=ch.dst, weight=ch.weight,
                         delay=ch.delay, angle=ch.angle, lines=ch.lines,
                         plastic=False)
            )
    return twin


def _exact_write_projection(field: Field, module: Module) -> None:
    """Recompute the write cone as the exact fixpoint of its afferents.

    The intra-slot channel graph is a shallow DAG (the corefold pyramid), so
    a few in-order sweeps of v_i <- Â_i settle it exactly. This is the same
    fixpoint continuous flow relaxes toward, computed algebraically so that
    counterfactual probes carry no metastable-equilibrium artifacts (an
    antipodal intervention exerts zero Kuramoto torque under flow, which
    would spuriously read as survival).
    """
    from .algebra import phase as _phase

    for _ in range(4):
        aff = field.afferents(module)
        for i in module.write_cone:
            a = aff[i]
            if abs(a) > 0.0:
                module.cells[i].theta = _phase(a)
                module.cells[i].amp = abs(a)


def cf_agreement(field: Field, name: str) -> float:
    """a: counterfactual survival fraction over read-cone interventions.

    For each read cell i: twin the module (twin network), intervene
    do(theta_i := theta_i + π) with the intervened cell latched, recompute
    the corefold pyramid exactly, re-quantize, and check whether the
    *singular* conclusion (the middle write cell's trit) survives.
    a = survivals / interventions. See the module docstring for the
    semantics and the structural 2/3 ceiling for single-cluster conclusions.
    """
    module = field.modules[name]
    singular_pos = module.write_cone[len(module.write_cone) // 2]

    base_twin = _twin_field_single(field, name)
    _exact_write_projection(base_twin, base_twin.modules[name])
    base_singular = base_twin.modules[name].trits(field.deadband)[singular_pos]

    trials = 0
    survivals = 0
    for cell_index in module.read_cone:
        trials += 1
        twin = _twin_field_single(field, name)
        tm = twin.modules[name]
        # do(): flip the evidence cell to its opposite pole (latched)
        tm.cells[cell_index].theta = wrap_angle(
            tm.cells[cell_index].theta + math.pi
        )
        _exact_write_projection(twin, tm)
        if tm.trits(field.deadband)[singular_pos] == base_singular:
            survivals += 1
    return survivals / trials if trials else 1.0


def causal_lift(field: Field, name: str) -> float:
    """ell: normalized free-energy drop of evidence vs the vacuum twin."""
    module = field.modules[name]
    aff = field.afferents(module)
    phi_actual = field.phi(module, aff)
    phi_vacuum = field.phi(module, [0j for _ in module.cells])
    lift = (phi_vacuum - phi_actual) / (1.0 + abs(phi_vacuum))
    return max(0.0, min(1.0, lift))


def global_agreement(field: Field, slot_names: list[str], singular_index: int = 4) -> float:
    """S: phase-order magnitude over the slots' singular cells."""
    values = []
    for n in slot_names:
        m = field.modules[n]
        idx = singular_index if singular_index < len(m.cells) else len(m.cells) - 1
        values.append(m.cells[idx].value())
    return phase_order(values)


@dataclass
class SlotMetrics:
    slot: int
    coherence: float
    coverage: float
    stability: float
    cf_agreement: float
    causal_lift: float
    openness: float

    def to_json(self) -> dict:
        return {
            "slot": self.slot,
            "coherence": round(self.coherence, 6),
            "coverage": round(self.coverage, 6),
            "stability": round(self.stability, 6),
            "cf_agreement": round(self.cf_agreement, 6),
            "causal_lift": round(self.causal_lift, 6),
            "openness": round(self.openness, 6),
        }
