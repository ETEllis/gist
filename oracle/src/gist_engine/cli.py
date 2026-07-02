"""The `gist` command-line interface: the mechanism, standalone.

Session workflow (a session directory holds config.json + ledger.jsonl):

    gist init --dir ./session --prompt "your question"
    gist ingest --dir ./session --file atoms.jsonl        # or --content ...
    gist step --dir ./session [-n CYCLES]
    gist run --dir ./session
    gist status --dir ./session
    gist intents --dir ./session
    gist fulfill --dir ./session --intent ID --file atoms.jsonl
    gist release --dir ./session
    gist export --dir ./session --format json|replay|markdown
    gist verify --path ./session/ledger.jsonl             # third-party replay
    gist demo [--dir ./demo-session]                      # full deterministic run
    gist census                                           # n=6 walk spectrum
    gist bridge --dyadic 101101 | --triadic 231 | --trits '+0-+0-'
    gist contract [--cdc path/to/gist.cdc]                # native contract check

Atoms file format: JSON Lines, each line
    {"content": "...", "polarity": 0.9, "salience": 0.8,
     "address": [q1, q2, q3], "provenance": {"url": "..."}}
(all fields except content optional; missing fields are hash-projected).

Because state is a pure fold over the ledger, every command reconstructs the
engine by replaying ledger inputs - there is no hidden state file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .bridge import (
    dyadic_of_index,
    dyadic_to_triadic,
    index_of_dyadic,
    project_trits,
    triadic_to_dyadic,
)
from .engine import GistConfig, GistEngine, verify_ledger
from .ledger import Ledger
from .ports import Atom
from .walks import census, from_word


def _session_paths(dir_: str) -> tuple[Path, Path, Path]:
    d = Path(dir_)
    return d, d / "config.json", d / "ledger.jsonl"


def _load_engine(dir_: str) -> GistEngine:
    """Rebuild the live engine by replaying the on-disk ledger's inputs.

    The replayed stream is compared against the recorded stream (full
    verification) before the engine adopts the file for future appends -
    a session directory can never silently drift from its ledger.
    """
    from .engine import replay_engine

    d, _cfg_path, ledger_path = _session_paths(dir_)
    if not ledger_path.exists():
        sys.exit(f"no session at {d} (run `gist init --dir {d} --prompt ...`)")
    try:
        recorded = Ledger.load(ledger_path)
    except Exception as err:
        sys.exit(f"ledger failed chain verification: {err}")
    engine = replay_engine(recorded)
    rec = [(e.kind, e.payload) for e in recorded]
    new = [(e.kind, e.payload) for e in engine.ledger]
    if rec != new:
        sys.exit("ledger failed replay verification; refusing to continue "
                 "(see `gist verify`)")
    engine.ledger.path = ledger_path  # adopt the file for future appends
    return engine


def _read_atoms(args: argparse.Namespace) -> list[Atom]:
    atoms: list[Atom] = []
    if getattr(args, "file", None):
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            atoms.append(
                Atom(
                    content=obj["content"],
                    polarity=obj.get("polarity"),
                    salience=obj.get("salience"),
                    address=tuple(obj["address"]) if obj.get("address") else None,
                    vector=tuple(obj["vector"]) if obj.get("vector") else None,
                    provenance=obj.get("provenance", {}),
                )
            )
    if getattr(args, "content", None):
        atoms.append(
            Atom(
                content=args.content,
                polarity=args.polarity,
                salience=args.salience,
                address=tuple(args.address) if args.address else None,
            )
        )
    if not atoms:
        sys.exit("no atoms given (use --file atoms.jsonl or --content ...)")
    return atoms


def _print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> None:
    d, cfg_path, ledger_path = _session_paths(args.dir)
    if ledger_path.exists():
        sys.exit(f"session already exists at {d}")
    d.mkdir(parents=True, exist_ok=True)
    config = GistConfig()
    if args.axes:
        parts = [a.strip() for a in args.axes.split(",")]
        if len(parts) != 3:
            sys.exit("--axes needs three comma-separated labels")
        config.axes = (parts[0], parts[1], parts[2])
    if args.budget is not None:
        config.retrieval_budget = args.budget
    engine = GistEngine(
        prompt=args.prompt,
        session_id=args.session,
        config=config,
        ledger_path=ledger_path,
    )
    cfg_path.write_text(json.dumps(config.to_json(), indent=2))
    print(f"session {engine.session_id} initialized at {d}")
    print(f"axes: {', '.join(config.axes)} | lattice: 64 slots (2^6 = 4^3)")


def cmd_ingest(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    atoms = _read_atoms(args)
    projected = engine.ingest(atoms)
    print(f"queued {len(projected)} atoms "
          f"(slots: {sorted({p.slot for p in projected})})")
    if args.step:
        summary = engine.step()
        _print(summary)


def cmd_step(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    for _ in range(args.n):
        summary = engine.step()
        _print(summary)
        if engine.release_record is not None:
            break


def cmd_run(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    release = engine.run(max_cycles=args.max_cycles)
    if release is not None:
        print("RELEASED")
        _print(
            {k: release[k] for k in
             ("tier", "root_word", "coordinate", "global_S", "stamp")}
        )
    else:
        v = engine.viability()
        print("no release yet")
        _print({"viability": v,
                "gate": engine.gate_report.to_json() if engine.gate_report else None})


def cmd_status(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    state = engine.state_json()
    if args.full:
        _print(state)
        return
    board = [b for b in state["board"] if b["atoms"] > 0]
    print(f"session {state['session_id']} | cycle {state['cycle']} | "
          f"S={state['S']} | ledger {state['ledger_length']} events")
    print(f"viability: {state['viability']['mode']} "
          f"(budget {state['viability']['budget_remaining']})")
    for b in board:
        m = b["metrics"] or {}
        print(
            f"  slot {b['slot']:>2} {b['dyadic']} ({b['triadic']}) "
            f"word={b['word']} tier={b['tier']:<11} "
            f"c={m.get('coverage', 0):.2f} u={m.get('stability', 0):.2f} "
            f"a={m.get('cf_agreement', 0):.2f} l={m.get('causal_lift', 0):.2f} "
            f"{'SAT' if b['saturated'] else ('intent:' + b['open_intent'] if b['open_intent'] else 'open')}"
        )
    if state["gate"]:
        checks = {c["name"]: c["passed"] for c in state["gate"]["checks"]}
        print("gate:", " ".join(f"{k}={'Y' if v else 'N'}" for k, v in checks.items()))
    if state["release"]:
        print(f"RELEASED tier={state['release']['tier']} "
              f"coordinate={state['release']['coordinate']['triadic']} "
              f"stamp={state['release']['stamp'][:16]}...")


def cmd_intents(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    _print(engine.state_json()["intents"])


def cmd_fulfill(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    atoms = _read_atoms(args) if (args.file or args.content) else []
    engine.fulfill(args.intent, atoms)
    print(f"fulfilled {args.intent} with {len(atoms)} atoms")
    if args.step:
        _print(engine.step())


def cmd_release(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    if engine.release_record is None:
        sys.exit("no release yet (see `gist status`, `gist run`)")
    _print(engine.release_record)


def cmd_export(args: argparse.Namespace) -> None:
    engine = _load_engine(args.dir)
    if args.format == "json":
        _print(engine.state_json())
    elif args.format == "replay":
        _print(engine.export_replay())
    elif args.format == "markdown":
        print(_markdown_report(engine))
    else:
        sys.exit(f"unknown format {args.format}")


def cmd_verify(args: argparse.Namespace) -> None:
    report = verify_ledger(args.path)
    _print(report)
    sys.exit(0 if report["verified"] else 1)


def cmd_census(args: argparse.Namespace) -> None:
    _print(census(args.arity))


def cmd_bridge(args: argparse.Namespace) -> None:
    if args.trits:
        row = project_trits(from_word(args.trits))
        _print({"trits": args.trits, "dyadic": row.dyadic,
                "triadic": row.triadic, "index": row.index})
    elif args.dyadic:
        _print({"dyadic": args.dyadic,
                "triadic": dyadic_to_triadic(args.dyadic),
                "index": index_of_dyadic(args.dyadic)})
    elif args.triadic:
        d = triadic_to_dyadic(args.triadic)
        _print({"triadic": args.triadic, "dyadic": d,
                "index": index_of_dyadic(d)})
    else:
        rows = [
            {"index": i, "dyadic": dyadic_of_index(i),
             "triadic": dyadic_to_triadic(dyadic_of_index(i))}
            for i in range(64)
        ]
        _print(rows)


def cmd_demo(args: argparse.Namespace) -> None:
    from .democorpus import PROMPT, build_corpus, drive

    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    ledger_path = d / "ledger.jsonl"
    if ledger_path.exists():
        sys.exit(f"demo session already exists at {d}")
    engine = GistEngine(prompt=PROMPT, session_id="gist-demo",
                        ledger_path=ledger_path)
    initial, reserve = build_corpus()
    engine.ingest(initial)
    release = drive(engine, reserve)
    print(_markdown_report(engine))
    replay_path = d / "frontend_replay.json"
    replay_path.write_text(
        json.dumps(engine.export_replay(), indent=2, ensure_ascii=False)
    )
    print(f"\nledger:  {ledger_path}")
    print(f"replay:  {replay_path}")
    report = verify_ledger(ledger_path)
    print(f"replay verification: "
          f"{'VERIFIED' if report['verified'] else 'FAILED'} "
          f"({report['events']} events)")
    sys.exit(0 if (release is not None and report["verified"]) else 1)


def cmd_contract(args: argparse.Namespace) -> None:
    from .contract import verify_contract

    report = verify_contract(args.cdc)
    for check in report["checks"]:
        mark = "ok " if check["passed"] else "FAIL"
        print(f"[{mark}] {check['witness']}: {check['claim']}")
    print(f"\n{report['passed']}/{report['total']} witnesses verified; "
          f"expectations: {report['expectations_ok']}")
    sys.exit(0 if report["verified"] else 1)


def _markdown_report(engine: GistEngine) -> str:
    state = engine.state_json()
    lines = [
        "# GIST SYNTHESIS BOARD",
        "",
        f"**Session:** {state['session_id']}  ",
        f"**Prompt:** {state['prompt']}  ",
        f"**Cycle:** {state['cycle']} | **Global agreement S:** {state['S']} | "
        f"**Ledger:** {state['ledger_length']} events (head "
        f"`{state['ledger_head'][:16]}...`)",
        "",
        "## Contributing scopes",
        "",
        "| Slot | Address | Word | Tier | c | u | a | lift | state |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for b in state["board"]:
        if b["atoms"] == 0:
            continue
        m = b["metrics"] or {}
        status = "saturated" if b["saturated"] else (
            "intent" if b["open_intent"] else "open")
        lines.append(
            f"| {b['slot']} | `{b['dyadic']}` ({b['triadic']}) | `{b['word']}` "
            f"| {b['tier']} | {m.get('coverage', 0):.2f} "
            f"| {m.get('stability', 0):.2f} | {m.get('cf_agreement', 0):.2f} "
            f"| {m.get('causal_lift', 0):.2f} | {status} |"
        )
    if state["gate"]:
        lines += ["", "## Gate", ""]
        for c in state["gate"]["checks"]:
            lines.append(f"- {'PASS' if c['passed'] else 'FAIL'} "
                         f"**{c['name']}** - {c['detail']}")
    if state["release"]:
        r = state["release"]
        lines += [
            "",
            "## RELEASE",
            "",
            f"- headline tier: **{r['tier']}** "
            f"(histogram: {r['tier_histogram']})",
            f"- root word: `{r['root_word']}` ({r['root_tier']})",
            f"- decision coordinate: `{r['coordinate']['dyadic']}` -> "
            f"triadic `{r['coordinate']['triadic']}` "
            f"(cell {r['coordinate']['index']})",
            f"- budget release: {r['budget_release']}",
            f"- Merkle leaf root: `{r['leaf_root']}`",
            f"- decision stamp: `{r['stamp']}`",
            "",
            "Replay-verify anytime: `gist verify --path <ledger.jsonl>`",
        ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="gist",
        description=f"GIST engine v{__version__} - Gated Insight Synthesis "
        "Topology (built on the BiDi Coherence-Delta Calculus)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init", help="create a session")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--prompt", required=True)
    sp.add_argument("--session", default=None)
    sp.add_argument("--axes", default=None,
                    help="three comma-separated axis labels")
    sp.add_argument("--budget", type=int, default=None)
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("ingest", help="queue evidence atoms")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--file")
    sp.add_argument("--content")
    sp.add_argument("--polarity", type=float, default=None)
    sp.add_argument("--salience", type=float, default=None)
    sp.add_argument("--address", type=int, nargs=3, default=None)
    sp.add_argument("--step", action="store_true", help="run a cycle after")
    sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser("step", help="run n cycles")
    sp.add_argument("--dir", required=True)
    sp.add_argument("-n", type=int, default=1)
    sp.set_defaults(func=cmd_step)

    sp = sub.add_parser("run", help="run to release or quiescence")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--max-cycles", type=int, default=64)
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("status", help="board summary")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--full", action="store_true")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("intents", help="open retrieval intents")
    sp.add_argument("--dir", required=True)
    sp.set_defaults(func=cmd_intents)

    sp = sub.add_parser("fulfill", help="answer an intent with atoms")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--intent", required=True)
    sp.add_argument("--file")
    sp.add_argument("--content")
    sp.add_argument("--polarity", type=float, default=None)
    sp.add_argument("--salience", type=float, default=None)
    sp.add_argument("--address", type=int, nargs=3, default=None)
    sp.add_argument("--step", action="store_true")
    sp.set_defaults(func=cmd_fulfill)

    sp = sub.add_parser("release", help="show the release record")
    sp.add_argument("--dir", required=True)
    sp.set_defaults(func=cmd_release)

    sp = sub.add_parser("export", help="export state/replay/markdown")
    sp.add_argument("--dir", required=True)
    sp.add_argument("--format", default="json",
                    choices=("json", "replay", "markdown"))
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("verify", help="third-party replay verification")
    sp.add_argument("--path", required=True)
    sp.set_defaults(func=cmd_verify)

    sp = sub.add_parser("census", help="balanced-ternary walk spectrum")
    sp.add_argument("--arity", type=int, default=6)
    sp.set_defaults(func=cmd_census)

    sp = sub.add_parser("bridge", help="dyadic/triadic bridge lookups")
    sp.add_argument("--dyadic")
    sp.add_argument("--triadic")
    sp.add_argument("--trits")
    sp.set_defaults(func=cmd_bridge)

    sp = sub.add_parser("demo", help="run the deterministic demo session")
    sp.add_argument("--dir", default="./gist-demo-session")
    sp.set_defaults(func=cmd_demo)

    sp = sub.add_parser("contract", help="verify the native gist.cdc contract")
    sp.add_argument("--cdc", default=None)
    sp.set_defaults(func=cmd_contract)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
