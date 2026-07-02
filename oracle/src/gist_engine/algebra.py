"""The coherence algebra C = (C, interfere, void, rotate, amplitude, kappa).

This is the carrier layer of the BiDi Coherence-Delta Calculus (CDC), in its
standard model C = R^2 realized as Python complex numbers:

    interfere  (⊞)  superposition        -> complex addition
    void       (⊥)  the empty value      -> 0j
    rotate     (⟳)  circle action        -> multiplication by e^{i·phi}
    amplitude  (|·|) seminorm            -> abs()
    kappa      (κ)  commitment cosine    -> Re(z)/|z|, kappa(void) = 0

Derived balanced-ternary predicates (deadband delta, canonically 1/2):

    trit      tau(z) = +1 if kappa >  delta
                       -1 if kappa < -delta
                        0 otherwise
    openness  vkappa(z) = max(0, 1 - |kappa|/delta)

The committed carrier is balanced ternary around real equilibrium:
-1 + 0 + 1 = 0. The middle value 0 is a live crossing (maximal openness),
not binary false.

Operator algebra (laws witnessed in tests/test_algebra_laws.py and by the
`gist contract` verifier):

    gate      (⊙)  phase-add on phase vectors  -> abelian group ≅ T^n
    interfere (⊞)  superpose                   -> commutative monoid
    rotate    (⟳)  global phase advance        -> ⊞-linear
    corefold  (∂)  distill middles             -> ⊞-linear, ⟳-equivariant,
                                                  strictly abstracting

Everything in this file is dependency-free and exact up to float arithmetic.
"""

from __future__ import annotations

import cmath
import math
from typing import Iterable, Sequence

# ---------------------------------------------------------------------------
# Carrier
# ---------------------------------------------------------------------------

Coh = complex          # a coherence value: amplitude * e^{i*theta}
VOID: Coh = 0j         # ⊥, the unit of interference

DEADBAND_CANONICAL = 0.5

TWO_PI = 2.0 * math.pi


def coh(amplitude: float, theta: float) -> Coh:
    """Construct a coherence value from polar form <a, theta>."""
    return complex(amplitude * math.cos(theta), amplitude * math.sin(theta))


def interfere(*values: Coh) -> Coh:
    """⊞ superposition: commutative monoid with unit VOID."""
    total: Coh = VOID
    for v in values:
        total += v
    return total


def rotate(phi: float, value: Coh) -> Coh:
    """⟳_phi rotation action of the circle T = R/2πZ by ⊞-automorphisms."""
    return value * cmath.exp(1j * phi)


def amplitude(value: Coh) -> float:
    """|·| amplitude seminorm: |VOID| = 0, rotation-invariant, subadditive."""
    return abs(value)


def phase(value: Coh) -> float:
    """arg of the value; phase(VOID) = 0.0 by convention."""
    if value == VOID:
        return 0.0
    return cmath.phase(value)


def kappa(value: Coh) -> float:
    """κ commitment cosine in [-1, 1]; κ(VOID) = 0 (pure aperture)."""
    a = abs(value)
    if a == 0.0:
        return 0.0
    return value.real / a


def trit(value: Coh, deadband: float = DEADBAND_CANONICAL) -> int:
    """tau: derived balanced-ternary runtime symbol of a coherence value."""
    k = kappa(value)
    if k > deadband:
        return 1
    if k < -deadband:
        return -1
    return 0


def openness(value: Coh, deadband: float = DEADBAND_CANONICAL) -> float:
    """vkappa boundary openness in [0, 1]; maximal at the crossing κ = 0."""
    return max(0.0, 1.0 - abs(kappa(value)) / deadband)


def wrap_angle(a: float) -> float:
    """Wrap an angle to (-pi, pi]."""
    a = math.fmod(a + math.pi, TWO_PI)
    if a <= 0.0:
        a += TWO_PI
    return a - math.pi


def pole_angle(value: Coh) -> float | None:
    """Nearest committed pole (0 for κ>0, π for κ<0); None at the crossing."""
    k = kappa(value)
    if k > 0.0:
        return 0.0
    if k < 0.0:
        return math.pi
    return None


# ---------------------------------------------------------------------------
# Gate ⊙ : the abelian phase group on phase vectors (≅ T^n)
# ---------------------------------------------------------------------------

PhaseVec = tuple[float, ...]


def gate(a: PhaseVec, b: PhaseVec) -> PhaseVec:
    """⊙ rotation-compose: componentwise phase addition on the torus."""
    if len(a) != len(b):
        raise ValueError("gate requires equal-arity phase vectors")
    return tuple(wrap_angle(x + y) for x, y in zip(a, b))


def gate_identity(n: int) -> PhaseVec:
    """The group identity of ⊙ at arity n."""
    return tuple(0.0 for _ in range(n))


def gate_inverse(a: PhaseVec) -> PhaseVec:
    """The group inverse of ⊙ (the complement operator at saturation)."""
    return tuple(wrap_angle(-x) for x in a)


# ---------------------------------------------------------------------------
# Core-fold ∂ : distillation (⊞-linear, ⟳-equivariant, strictly abstracting)
# ---------------------------------------------------------------------------

def corefold_3_to_2(triad: Sequence[Coh]) -> tuple[Coh, Coh]:
    """∂ : C^3 -> C^2, the triad-to-dyad distillation.

    ((a+b)/2, (b+c)/2): each dyad cell is the superposition mean of an
    adjacent pair. Linear in ⊞ and equivariant under ⟳ (means commute with
    rotation); strictly abstracting (not injective, not idempotent).
    """
    a, b, c = triad
    return ((a + b) / 2.0, (b + c) / 2.0)


def corefold_2_to_1(dyad: Sequence[Coh]) -> Coh:
    """∂ : C^2 -> C^1, the dyad-to-singular distillation (superposition mean)."""
    u, v = dyad
    return (u + v) / 2.0


def corefold_middle(cells: Sequence[Coh]) -> Coh:
    """Module-level latent projection: distill the middle cells.

    For the canonical n=6 module [r0 r1 r2 | w0 w1 w2] the middle cells are
    indices 2 and 3 - the interface between read cone and write cone.
    """
    n = len(cells)
    if n < 2:
        return cells[0] if cells else VOID
    lo = (n - 1) // 2
    hi = n // 2
    if lo == hi:
        return cells[lo]
    return (cells[lo] + cells[hi]) / 2.0


# ---------------------------------------------------------------------------
# Phase-order magnitude (the coherence measure; Kuramoto order parameter)
# ---------------------------------------------------------------------------

def phase_order(values: Iterable[Coh]) -> float:
    """Amplitude-weighted mean resultant length in [0, 1].

    R = |Σ a_i e^{i θ_i}| / Σ a_i.  R = 1 means perfect phase alignment
    (maximal coherence); R -> 0 means incoherent superposition. This is the
    CDC 'phase-order magnitude' and the engine's coherence measure.
    """
    total = VOID
    mass = 0.0
    for v in values:
        total += v
        mass += abs(v)
    if mass == 0.0:
        return 0.0
    return abs(total) / mass


def coherence_delta(a: Coh, b: Coh) -> float:
    """The signed phase difference between two coherence values (the γΔ core).

    wrap(arg(a) - arg(b)); zero when the two reference frames agree.
    """
    return wrap_angle(phase(a) - phase(b))
