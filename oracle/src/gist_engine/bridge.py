"""The dyadic/triadic bridge: 2^6 = 4^3 = 64.

This is GIST's address system, taken directly from the CDC bootstrap bridge
codebook (`bridge64.cdc`). Every lattice slot has two equivalent names:

  dyadic   a six-bit word  b0 b1 b2 b3 b4 b5   (MSB first, as written)
  triadic  three base-4 digits (q1, q2, q3)    with q_i = 2*b_{2i} + b_{2i+1}

The three triadic digits are GIST's three semantic axes (by default:
temporal, abstraction, evidence-type - each with four values 0..3). The six
dyadic bits are the Hamming coordinates consumed one per round by the
meta-gate ladder 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1.

The bridge also carries the CDC trace projection (witnessed in
`native_surface.cdc`): a committed six-trit word projects to a bridge
coordinate through its *occupancy* (nonzero trit -> 1, crossing -> 0), e.g.
trits '+0-+0-' -> dyadic '101101' -> triadic '231' -> index 45.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from . import cdcread
from .walks import occupancy_bits

N_BITS = 6
N_SLOTS = 64


@dataclass(frozen=True)
class BridgeRow:
    index: int
    dyadic: str
    triadic: str


def dyadic_to_triadic(dyadic: str) -> str:
    """Map a 2n-bit dyadic word to its n/... base-4 triadic word (bit pairs)."""
    if len(dyadic) % 2 != 0 or any(c not in "01" for c in dyadic):
        raise ValueError(f"bad dyadic word: {dyadic!r}")
    digits = []
    for i in range(0, len(dyadic), 2):
        digits.append(str(2 * int(dyadic[i]) + int(dyadic[i + 1])))
    return "".join(digits)


def triadic_to_dyadic(triadic: str) -> str:
    """Map a base-4 triadic word back to its dyadic bit word."""
    if any(c not in "0123" for c in triadic):
        raise ValueError(f"bad triadic word: {triadic!r}")
    bits = []
    for c in triadic:
        q = int(c)
        bits.append(str((q >> 1) & 1))
        bits.append(str(q & 1))
    return "".join(bits)


def index_of_dyadic(dyadic: str) -> int:
    return int(dyadic, 2)


def dyadic_of_index(index: int, n_bits: int = N_BITS) -> str:
    if not 0 <= index < (1 << n_bits):
        raise ValueError(f"index out of range: {index}")
    return format(index, f"0{n_bits}b")


def triadic_of_index(index: int, n_bits: int = N_BITS) -> str:
    return dyadic_to_triadic(dyadic_of_index(index, n_bits))


def address_of_index(index: int) -> tuple[int, int, int]:
    """The (q1, q2, q3) axis coordinates of a 64-lattice slot."""
    t = triadic_of_index(index)
    return (int(t[0]), int(t[1]), int(t[2]))


def index_of_address(q1: int, q2: int, q3: int) -> int:
    for q in (q1, q2, q3):
        if not 0 <= q <= 3:
            raise ValueError(f"axis value out of range: {(q1, q2, q3)}")
    return index_of_dyadic(triadic_to_dyadic(f"{q1}{q2}{q3}"))


def generate_codebook(n_bits: int = N_BITS) -> list[BridgeRow]:
    """Generate the full 2^n = 4^(n/2) bridge codebook (n even)."""
    if n_bits % 2 != 0:
        raise ValueError("bridge arity must be even (n = 2k bits = k digits)")
    rows = []
    for i in range(1 << n_bits):
        d = dyadic_of_index(i, n_bits)
        rows.append(BridgeRow(index=i, dyadic=d, triadic=dyadic_to_triadic(d)))
    return rows


def verify_bijection(rows: Sequence[BridgeRow]) -> bool:
    """Check the codebook is a bijection both ways and index-consistent."""
    seen_d: set[str] = set()
    seen_t: set[str] = set()
    for row in rows:
        if row.dyadic in seen_d or row.triadic in seen_t:
            return False
        seen_d.add(row.dyadic)
        seen_t.add(row.triadic)
        if index_of_dyadic(row.dyadic) != row.index:
            return False
        if dyadic_to_triadic(row.dyadic) != row.triadic:
            return False
        if triadic_to_dyadic(row.triadic) != row.dyadic:
            return False
    return len(seen_d) == len(rows) and len(seen_t) == len(rows)


def project_trits(trits: Sequence[int]) -> BridgeRow:
    """Project a committed six-trit word into its bridge coordinate.

    Occupancy projection per the CDC trace/bridge witness:
    nonzero -> 1, crossing -> 0; then dyadic -> triadic through the codebook.
    """
    dyadic = occupancy_bits(trits)
    if len(dyadic) != N_BITS:
        raise ValueError(f"bridge projection needs 6 trits, got {len(dyadic)}")
    return BridgeRow(
        index=index_of_dyadic(dyadic),
        dyadic=dyadic,
        triadic=dyadic_to_triadic(dyadic),
    )


def load_bridge_cdc(path: str | Path) -> list[BridgeRow]:
    """Load bridge rows from a CDC-format bridge codebook file."""
    program = cdcread.parse_file(path)
    rows = []
    for d in program.all("witness"):
        dy = d.get("dyadic")
        tr = d.get("triadic")
        idx = d.get("index")
        if dy is None or tr is None or idx is None:
            continue
        rows.append(BridgeRow(index=int(idx), dyadic=dy, triadic=tr))
    rows.sort(key=lambda r: r.index)
    return rows


def parity_with_cdc(path: str | Path, n_bits: int = N_BITS) -> bool:
    """True iff a CDC bridge codebook file matches this engine's generation rule."""
    loaded = load_bridge_cdc(path)
    generated = generate_codebook(n_bits)
    return loaded == generated
