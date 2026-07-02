#!/usr/bin/env python3
"""Run the deterministic GIST demo session end to end.

Equivalent to `gist demo --dir ./gist-demo-session`, runnable directly from
a checkout:

    PYTHONPATH=src python3 demo/run_demo.py [output-dir]

Produces: the synthesis board (markdown), ledger.jsonl (the verifiable
session), and frontend_replay.json (the UI coupling bundle), then replay-
verifies the ledger from disk.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gist_engine.cli import main  # noqa: E402

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "./gist-demo-session"
    main(["demo", "--dir", out])
