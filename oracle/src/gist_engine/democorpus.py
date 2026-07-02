"""A deterministic, self-contained demonstration corpus.

Used by the CLI `gist demo`, the end-to-end tests, and the contract verifier.
No network, no model: every atom carries explicit address/polarity/salience,
so the whole pipeline - superposition, commits, plateau detection, retrieval
intents, fulfillment, saturation, gate, ladder, reconciliation, stamp,
release, replay verification - runs identically everywhere.

The corpus is shaped to exercise the mechanism honestly:

  - eight contributing scopes chosen so all three axes cover {0,1,2,3} and
    the parity classes (Σq mod 2 / mod 3) are non-degenerate;
  - each full scope carries a dominant supporting cluster plus a weaker
    opposing cluster (two phase-separated read cells: near-closed boundary,
    admissible committed word);
  - two scopes start with only the dominant cluster, so their boundary stays
    open (empty read cells are maximally open) -> the engine emits retrieval
    intents; the reserve fulfills them -> they close and saturate;
  - one scope receives near-balanced opposing evidence early (a contested,
    counterfactually fragile state) and a later clarifying reserve batch.
"""

from __future__ import annotations

from .engine import GistEngine
from .ports import Atom

PROMPT = (
    "Does distributed peer review improve the reliability of published "
    "findings?"
)

# (q1, q2, q3) scopes; see module docstring for the coverage/parity design.
FULL_SCOPES = [
    (0, 0, 0),
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3),
    (0, 0, 1),
    (0, 2, 3),
]
INTENT_SCOPES = [
    (1, 3, 3),
    (2, 3, 3),
]

_SUPPORT = [
    ("replication rates rise when review is distributed across independent "
     "referees ({}/{}/{})", 0.92, 0.85),
    ("error detection improves with reviewer diversity in scope {}/{}/{}",
     0.88, 0.80),
    ("post-publication distributed review catches methodological flaws "
     "earlier ({}/{}/{})", 0.90, 0.82),
]
_OPPOSE = [
    ("reviewer fatigue in distributed systems lowers per-review depth "
     "({}/{}/{})", -0.72, 0.40),
    ("diffusion of responsibility can weaken accountability in scope "
     "{}/{}/{}", -0.70, 0.38),
]


def _atoms_for(scope: tuple[int, int, int], include_oppose: bool) -> list[Atom]:
    out = []
    for text, pol, sal in _SUPPORT:
        out.append(
            Atom(
                content=text.format(*scope),
                polarity=pol,
                salience=sal,
                address=scope,
                provenance={"source": "seed-corpus"},
            )
        )
    if include_oppose:
        for text, pol, sal in _OPPOSE:
            out.append(
                Atom(
                    content=text.format(*scope),
                    polarity=pol,
                    salience=sal,
                    address=scope,
                    provenance={"source": "seed-corpus"},
                )
            )
    return out


def build_corpus() -> tuple[list[Atom], dict[tuple[int, int, int], list[Atom]]]:
    """Returns (initial_atoms, reserve_by_scope)."""
    initial: list[Atom] = []
    for scope in FULL_SCOPES:
        initial.extend(_atoms_for(scope, include_oppose=True))
    for scope in INTENT_SCOPES:
        initial.extend(_atoms_for(scope, include_oppose=False))
    reserve = {
        scope: [
            Atom(
                content=text.format(*scope),
                polarity=pol,
                salience=sal,
                address=scope,
                provenance={"source": "reserve-corpus", "via": "retrieval"},
            )
            for text, pol, sal in _OPPOSE
        ]
        for scope in INTENT_SCOPES
    }
    return initial, reserve


def drive(
    engine: GistEngine,
    reserve: dict[tuple[int, int, int], list[Atom]],
    max_cycles: int = 48,
) -> dict | None:
    """A minimal deterministic host loop: step, answer intents from reserve.

    This is what any embedding platform does around the engine - the
    mechanism asks, the host answers - here with a static corpus instead of
    a search backend.
    """
    reserve = {k: list(v) for k, v in reserve.items()}
    for _ in range(max_cycles):
        if engine.release_record is not None:
            break
        engine.step()
        for intent in list(engine.open_intents()):
            atoms = reserve.pop(intent.address, None)
            if atoms is not None:
                engine.fulfill(intent.intent_id, atoms)
            else:
                engine.fulfill(intent.intent_id, [])  # honest "nothing found"
    return engine.release_record
