"""Balanced-ternary trit walks: the barrier invariant and the normal-form spectrum.

A committed module yields a word of trits (t_1 .. t_n), each in {-1, 0, +1}.
Its *walk* is the prefix sum r_0 = 0, r_i = r_{i-1} + t_i.

CDC invariants realized here:

  admissible   the walk never goes negative (nonnegative balance invariant;
               metatheorem T1 Preservation - the commit barrier enforces it)
  localized    admissible AND returns to 0 (a T5 normal form: a *value*)
  saturated    every trit is nonzero AND the word sums to 0
  catalan      saturated AND admissible (the strongest closed filament)

The finite n=6 spectrum is the calculus's normal-form census, inherited by
GIST as its release-tier system:

  total 729 = 3^6         all trit words
  admissible 267          directed-animal count
  localized 51            Motzkin M_6
  saturated 20            central binomial C(6,3)
  catalan 5               Catalan C_3

(These exact counts are declared in the CDC native source
`native_reducer.cdc` under `proof trit-walk-n6` and re-verified here by
`census(6)` in tests and by the `gist contract` verifier.)
"""

from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence

Trits = tuple[int, ...]

TRIT_CHARS = {1: "+", 0: "0", -1: "-"}
CHAR_TRITS = {"+": 1, "0": 0, "-": -1}


def to_word(trits: Sequence[int]) -> str:
    """Render trits as a CDC word, e.g. (0, 1, -1) -> '0+-'."""
    return "".join(TRIT_CHARS[t] for t in trits)


def from_word(word: str) -> Trits:
    """Parse a CDC trit word, e.g. '0+-' -> (0, 1, -1)."""
    return tuple(CHAR_TRITS[c] for c in word)


def walk(trits: Sequence[int]) -> tuple[int, ...]:
    """Prefix-sum walk r_1..r_n of a trit word."""
    out: list[int] = []
    r = 0
    for t in trits:
        r += t
        out.append(r)
    return tuple(out)


def is_admissible(trits: Sequence[int]) -> bool:
    """Nonnegative balance invariant: no prefix of the walk goes below 0."""
    r = 0
    for t in trits:
        r += t
        if r < 0:
            return False
    return True


def first_violation(trits: Sequence[int]) -> int | None:
    """Index (0-based) of the first cell that forces the walk negative, else None.

    This is the exact attribution used by VDR (veto-diff-repair) hints: the
    commit barrier knows precisely which cell created negative coherence debt.
    """
    r = 0
    for i, t in enumerate(trits):
        r += t
        if r < 0:
            return i
    return None


def is_localized(trits: Sequence[int]) -> bool:
    """A T5 normal form: admissible and the walk returns to 0."""
    return is_admissible(trits) and sum(trits) == 0


def is_saturated(trits: Sequence[int]) -> bool:
    """Every cell decisively polarized (no crossings) and balanced to 0."""
    return all(t != 0 for t in trits) and sum(trits) == 0


def is_catalan(trits: Sequence[int]) -> bool:
    """Saturated and admissible: a closed, never-indebted, fully decisive word."""
    return is_saturated(trits) and is_admissible(trits)


def classify(trits: Sequence[int]) -> str:
    """Headline release tier of a committed word.

    catalan > saturated > localized > admissible > inadmissible.
    ('saturated' here as a *tier* means saturated-and-admissible but not
    returning-through-crossings; an inadmissible saturated word still reports
    'inadmissible' because the barrier outranks everything.)
    """
    if not is_admissible(trits):
        return "inadmissible"
    if is_catalan(trits):
        return "catalan"
    if is_localized(trits):
        return "localized"
    return "admissible"


TIER_ORDER = ["inadmissible", "admissible", "localized", "catalan"]


def tier_rank(tier: str) -> int:
    return TIER_ORDER.index(tier)


def census(n: int) -> dict[str, int]:
    """Exhaustive spectrum census over all 3^n trit words.

    census(6) must equal the CDC native proof expectations:
    {'total': 729, 'admissible': 267, 'localized': 51,
     'saturated': 20, 'catalan': 5}
    """
    total = admissible = localized = saturated = catalan = 0
    for word in product((-1, 0, 1), repeat=n):
        total += 1
        adm = is_admissible(word)
        if adm:
            admissible += 1
        if adm and sum(word) == 0:
            localized += 1
        if all(t != 0 for t in word) and sum(word) == 0:
            saturated += 1
            if adm:
                catalan += 1
    return {
        "total": total,
        "admissible": admissible,
        "localized": localized,
        "saturated": saturated,
        "catalan": catalan,
    }


CDC_N6_SPECTRUM = {
    "total": 729,
    "admissible": 267,
    "localized": 51,
    "saturated": 20,
    "catalan": 5,
}


def occupancy_bits(trits: Iterable[int]) -> str:
    """Project a trit word to its dyadic occupancy: nonzero -> 1, crossing -> 0.

    This is the CDC trace-to-bridge projection witnessed in
    `native_surface.cdc`: trits '+0-+0-' project to dyadic '101101'.
    """
    return "".join("1" if t != 0 else "0" for t in trits)
