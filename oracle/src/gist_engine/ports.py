"""Ports: the seams where GIST couples to anything above it.

GIST is a *mechanism*: it computes coherence over phase geometry. What maps
meaning onto geometry - and what fetches new evidence - is deliberately a
port, so the same engine embeds under any product platform, agent runtime,
or UI without modification:

  Projector        semantics -> geometry. Maps an Atom to a lattice address
                   (which slot), a polarity (which pole the evidence points
                   toward), and a salience (how much amplitude it carries).
                   Defaults: caller-specified fields pass through; anything
                   unspecified is derived deterministically (HashProjector),
                   so the engine runs standalone with real dynamics and full
                   verifiability even with no model attached. VectorProjector
                   accepts embedding vectors for production semantic routing.

  RetrievalIntent  the engine's outward ask. Emitted when a slot plateaus
                   with an open boundary (cells at their crossing - the CDC
                   state of maximal openness to relation). A host fulfills it
                   with more Atoms (web search, RAG, human input, database);
                   the engine never performs IO itself.

  EscalationIntent the degeneracy signal (GIST's model-escalation hook):
                   emitted when fulfillments keep arriving but the slot stays
                   open - the host may route the scope to a stronger reactor.

All ports are optional. The engine is complete and executable without any.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Protocol, Sequence

from .bridge import N_SLOTS, index_of_address, address_of_index


@dataclass(frozen=True)
class Atom:
    """One unit of evidence entering the lattice.

    content   the claim/observation text (or an opaque reference);
    polarity  [-1, +1]: sign and strength of support for the slot's thesis
              pole (+1 fully supports, -1 fully contradicts, 0 orthogonal);
    salience  [0, 1]: evidence weight (source quality, relevance);
    address   optional (q1, q2, q3) lattice coordinates; None = project;
    vector    optional embedding vector for vector-based projection;
    provenance optional source record (url, doi, citation, hash...).
    """

    content: str
    polarity: float | None = None
    salience: float | None = None
    address: tuple[int, int, int] | None = None
    vector: tuple[float, ...] | None = None
    provenance: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ProjectedAtom:
    """An atom after projection: geometry the field can superpose."""

    content: str
    slot: int                   # lattice index 0..63
    polarity: float             # [-1, 1]
    salience: float             # [0, 1]
    theta: float                # phase in the slot frame: arccos-like of polarity
    amplitude: float            # = salience
    provenance: dict[str, str] = field(default_factory=dict)

    @property
    def address(self) -> tuple[int, int, int]:
        return address_of_index(self.slot)


class Projector(Protocol):
    """semantics -> geometry port."""

    def project(self, atom: Atom) -> ProjectedAtom: ...


def _hash_unit(content: str, label: str) -> float:
    """Deterministic uniform-ish value in [0, 1) from content."""
    digest = hashlib.sha256(f"{label}\x1f{content}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def polarity_to_theta(polarity: float) -> float:
    """Map polarity in [-1, 1] to a phase in the slot's thesis frame.

    +1 -> 0 (the + pole), -1 -> π (the - pole), 0 -> π/2 (the crossing:
    orthogonal evidence sits at the aperture). theta = arccos(polarity).
    """
    p = max(-1.0, min(1.0, polarity))
    return math.acos(p)


class HashProjector:
    """Deterministic, dependency-free default projection.

    Uses caller-provided address/polarity/salience when present; derives any
    missing piece from SHA-256 of the content. This makes the mechanism fully
    runnable and replay-verifiable standalone: no model in the loop, no IO.
    """

    def project(self, atom: Atom) -> ProjectedAtom:
        if atom.address is not None:
            slot = index_of_address(*atom.address)
        else:
            slot = int(_hash_unit(atom.content, "slot") * N_SLOTS) % N_SLOTS
        polarity = (
            atom.polarity
            if atom.polarity is not None
            else (2.0 * _hash_unit(atom.content, "polarity") - 1.0)
        )
        salience = (
            atom.salience
            if atom.salience is not None
            else 0.25 + 0.75 * _hash_unit(atom.content, "salience")
        )
        polarity = max(-1.0, min(1.0, polarity))
        salience = max(0.0, min(1.0, salience))
        return ProjectedAtom(
            content=atom.content,
            slot=slot,
            polarity=polarity,
            salience=salience,
            theta=polarity_to_theta(polarity),
            amplitude=salience,
            provenance=dict(atom.provenance),
        )


class VectorProjector:
    """Embedding-vector projection: the production seam for LLM/embedding hosts.

    The host supplies, per axis, four anchor vectors (one per axis value 0-3).
    An atom's vector routes to the axis value whose anchor it most aligns
    with (cosine); polarity defaults to the alignment sign against the
    winning anchor of axis 3 unless given; salience defaults to vector norm
    saturation unless given. Falls back to HashProjector for vector-less atoms.
    """

    def __init__(self, axis_anchors: Sequence[Sequence[Sequence[float]]]):
        if len(axis_anchors) != 3 or any(len(a) != 4 for a in axis_anchors):
            raise ValueError("axis_anchors must be 3 axes x 4 anchor vectors")
        self.axis_anchors = [
            [tuple(float(x) for x in anchor) for anchor in axis]
            for axis in axis_anchors
        ]
        self._fallback = HashProjector()

    @staticmethod
    def _cos(a: Sequence[float], b: Sequence[float]) -> float:
        num = sum(x * y for x, y in zip(a, b))
        da = math.sqrt(sum(x * x for x in a))
        db = math.sqrt(sum(y * y for y in b))
        if da == 0.0 or db == 0.0:
            return 0.0
        return num / (da * db)

    def project(self, atom: Atom) -> ProjectedAtom:
        if atom.vector is None:
            return self._fallback.project(atom)
        digits = []
        best_align = 0.0
        for axis in self.axis_anchors:
            sims = [self._cos(atom.vector, anchor) for anchor in axis]
            best = max(range(4), key=lambda i: sims[i])
            digits.append(best)
            best_align = sims[best]
        slot = index_of_address(digits[0], digits[1], digits[2])
        polarity = atom.polarity if atom.polarity is not None else max(-1.0, min(1.0, best_align))
        norm = math.sqrt(sum(x * x for x in atom.vector))
        salience = atom.salience if atom.salience is not None else (1.0 - math.exp(-norm))
        salience = max(0.0, min(1.0, salience))
        return ProjectedAtom(
            content=atom.content,
            slot=slot,
            polarity=polarity,
            salience=salience,
            theta=polarity_to_theta(polarity),
            amplitude=salience,
            provenance=dict(atom.provenance),
        )


@dataclass(frozen=True)
class RetrievalIntent:
    """The engine asking its host for evidence it cannot synthesize internally."""

    intent_id: str
    slot: int
    address: tuple[int, int, int]
    openness: float               # mean read-cone openness (why we're asking)
    coherence: float              # current slot coherence (where we plateaued)
    gap_cells: tuple[int, ...]    # read cells sitting at their crossing
    query_hint: str               # axis-labelled ask the host can turn into a query
    fulfillments: int = 0


@dataclass(frozen=True)
class EscalationIntent:
    """Degeneracy signal: repeated fulfillment hasn't closed the slot's aperture."""

    intent_id: str
    slot: int
    address: tuple[int, int, int]
    attempts: int
    openness: float
