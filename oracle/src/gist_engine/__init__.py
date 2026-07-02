"""gist-engine: GIST (Gated Insight Synthesis Topology).

An executable synthesis mechanism derived from first principles out of the
BiDi Coherence-Delta Calculus: a 64-slot (2^6 = 4^3) lattice of balanced-
ternary coherence modules, reduced by guarded commits, a six-round Hamming
ladder whose reduction tree is its own Merkle tree, and a council-reconciled,
HKDF/HMAC-stamped, replay-verifiable release.

Public API:

    from gist_engine import GistEngine, GistConfig, Atom
    eng = GistEngine(prompt="...", ledger_path="session.jsonl")
    eng.ingest([Atom(content="...", polarity=0.8, salience=0.9,
                     address=(1, 2, 3))])
    release = eng.run()
    eng.state_json()                  # frontend/host coupling surface
    for intent in eng.open_intents(): # the engine asking for evidence
        eng.fulfill(intent.intent_id, more_atoms)

    from gist_engine import verify_ledger
    verify_ledger("session.jsonl")    # third-party replay verification
"""

__version__ = "1.1.0"

from .engine import GistConfig, GistEngine, verify_ledger  # noqa: E402
from .gate import GateThresholds  # noqa: E402
from .neural import GistNeural  # noqa: E402
from .ports import (  # noqa: E402
    Atom,
    EscalationIntent,
    HashProjector,
    ProjectedAtom,
    Projector,
    RetrievalIntent,
    VectorProjector,
)
from .reasonloop import ReasonLoop, StepFeedback, pre_gate  # noqa: E402
from .verdict import (  # noqa: E402
    TOOL_SPEC,
    Verdict,
    as_tool_call,
    conclude,
    verdict,
)

__all__ = [
    "__version__",
    "GistEngine",
    "GistConfig",
    "GateThresholds",
    "GistNeural",
    "Atom",
    "ProjectedAtom",
    "Projector",
    "HashProjector",
    "VectorProjector",
    "RetrievalIntent",
    "EscalationIntent",
    "verify_ledger",
    "Verdict",
    "verdict",
    "conclude",
    "TOOL_SPEC",
    "as_tool_call",
    "ReasonLoop",
    "StepFeedback",
    "pre_gate",
]
