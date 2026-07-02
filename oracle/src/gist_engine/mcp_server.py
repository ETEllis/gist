"""MCP bolt-on: the GIST engine as a Model Context Protocol server.

Zero dependencies - a newline-delimited JSON-RPC 2.0 loop over stdio
implementing the MCP surface (initialize, tools/list, tools/call, ping).

Run:
    python3 -m gist_engine.mcp_server

Claude Desktop / Claude Code style registration:
    { "mcpServers": { "gist": {
        "command": "python3", "args": ["-m", "gist_engine.mcp_server"] } } }

Tools exposed:

  gist_verdict   one-shot ternary bridge: claim + evidence -> yes/no/maybe
                 with asks (see verdict.py)
  gist_open      open a persistent lattice session (returns session id)
  gist_ingest    add evidence atoms to a session
  gist_step      run n cycles
  gist_state     the full board projection (JSON)
  gist_intents   open retrieval intents (what the engine is asking for)
  gist_fulfill   answer an intent with atoms
  gist_release   the stamped release record, if released
  gist_verify    third-party replay verification of a ledger file

Sessions are in-memory by default; pass "ledger_path" to gist_open for a
persistent, replay-verifiable JSONL ledger.
"""

from __future__ import annotations

import json
import sys
from typing import Any, TextIO

from . import __version__
from .engine import GistConfig, GistEngine, verify_ledger
from .ports import Atom
from .verdict import TOOL_SPEC, as_tool_call, verdict_config

PROTOCOL_VERSION = "2025-06-18"

_SESSIONS: dict[str, GistEngine] = {}


def _atom_items_schema() -> dict[str, Any]:
    return TOOL_SPEC["input_schema"]["properties"]["atoms"]


def tool_definitions() -> list[dict[str, Any]]:
    atoms_schema = _atom_items_schema()
    session_prop = {"session_id": {"type": "string"}}
    return [
        {
            "name": TOOL_SPEC["name"],
            "description": TOOL_SPEC["description"],
            "inputSchema": TOOL_SPEC["input_schema"],
        },
        {
            "name": "gist_open",
            "description": "Open a persistent GIST lattice session.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "session_id": {"type": "string"},
                    "ledger_path": {"type": "string"},
                    "gate_scope": {"type": "string",
                                   "enum": ["full", "occupied"]},
                },
                "required": ["prompt"],
            },
        },
        {
            "name": "gist_ingest",
            "description": "Queue evidence atoms into a session "
                           "(processed on the next step).",
            "inputSchema": {
                "type": "object",
                "properties": {**session_prop, "atoms": atoms_schema},
                "required": ["session_id", "atoms"],
            },
        },
        {
            "name": "gist_step",
            "description": "Run n engine cycles (default 1).",
            "inputSchema": {
                "type": "object",
                "properties": {**session_prop, "n": {"type": "integer"}},
                "required": ["session_id"],
            },
        },
        {
            "name": "gist_state",
            "description": "Full board projection: 64 slots, metrics, gate, "
                           "intents, release, viability.",
            "inputSchema": {"type": "object", "properties": session_prop,
                            "required": ["session_id"]},
        },
        {
            "name": "gist_intents",
            "description": "Open retrieval intents - what the engine asks "
                           "its host to find.",
            "inputSchema": {"type": "object", "properties": session_prop,
                            "required": ["session_id"]},
        },
        {
            "name": "gist_fulfill",
            "description": "Answer a retrieval intent with atoms "
                           "(empty atoms = honest 'nothing found').",
            "inputSchema": {
                "type": "object",
                "properties": {
                    **session_prop,
                    "intent_id": {"type": "string"},
                    "atoms": atoms_schema,
                },
                "required": ["session_id", "intent_id"],
            },
        },
        {
            "name": "gist_release",
            "description": "The stamped release record, or the gate report "
                           "if not yet released.",
            "inputSchema": {"type": "object", "properties": session_prop,
                            "required": ["session_id"]},
        },
        {
            "name": "gist_verify",
            "description": "Third-party replay verification of a session "
                           "ledger file.",
            "inputSchema": {
                "type": "object",
                "properties": {"ledger_path": {"type": "string"}},
                "required": ["ledger_path"],
            },
        },
    ]


def _atoms(specs: list[dict[str, Any]] | None) -> list[Atom]:
    out = []
    for s in specs or []:
        out.append(Atom(
            content=str(s["content"]),
            polarity=s.get("polarity"),
            salience=s.get("salience"),
            address=tuple(s["address"]) if s.get("address") else None,
            provenance=dict(s.get("provenance", {})),
        ))
    return out


def call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Dispatch a tool call; returns a JSON-safe result object."""
    if name == "gist_verdict":
        return json.loads(as_tool_call(args))
    if name == "gist_open":
        cfg = verdict_config() if args.get("gate_scope") == "occupied" \
            else GistConfig(gate_scope=args.get("gate_scope", "full"))
        engine = GistEngine(
            prompt=args["prompt"],
            session_id=args.get("session_id"),
            config=cfg,
            ledger_path=args.get("ledger_path"),
        )
        _SESSIONS[engine.session_id] = engine
        return {"session_id": engine.session_id,
                "axes": list(engine.config.axes),
                "gate_scope": engine.config.gate_scope}
    if name == "gist_verify":
        return verify_ledger(args["ledger_path"])

    engine = _SESSIONS.get(args.get("session_id", ""))
    if engine is None:
        raise KeyError(f"unknown session {args.get('session_id')!r}")
    if name == "gist_ingest":
        projected = engine.ingest(_atoms(args.get("atoms")))
        return {"queued": len(projected),
                "slots": sorted({p.slot for p in projected})}
    if name == "gist_step":
        out = [engine.step() for _ in range(max(1, int(args.get("n", 1))))]
        return {"cycles": out}
    if name == "gist_state":
        return engine.state_json()
    if name == "gist_intents":
        return {"intents": engine.state_json()["intents"]}
    if name == "gist_fulfill":
        engine.fulfill(args["intent_id"], _atoms(args.get("atoms")))
        return {"fulfilled": args["intent_id"]}
    if name == "gist_release":
        if engine.release_record is not None:
            return engine.release_record
        return {"released": False,
                "gate": engine.gate_report.to_json()
                if engine.gate_report else None,
                "viability": engine.viability()}
    raise KeyError(f"unknown tool {name!r}")


def handle_message(msg: dict[str, Any]) -> dict[str, Any] | None:
    """JSON-RPC 2.0 dispatch. Returns a response object or None (notification)."""
    method = msg.get("method")
    msg_id = msg.get("id")

    def result(payload: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id, "result": payload}

    def error(code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id,
                "error": {"code": code, "message": message}}

    if method == "initialize":
        return result({
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "gist-engine",
                           "version": __version__},
        })
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "ping":
        return result({})
    if method == "tools/list":
        return result({"tools": tool_definitions()})
    if method == "tools/call":
        params = msg.get("params", {})
        try:
            payload = call_tool(params.get("name", ""),
                                params.get("arguments", {}) or {})
            return result({
                "content": [{"type": "text",
                             "text": json.dumps(payload, ensure_ascii=False)}],
                "isError": False,
            })
        except Exception as exc:  # tool errors are results, not protocol errors
            return result({
                "content": [{"type": "text", "text": f"error: {exc}"}],
                "isError": True,
            })
    if msg_id is None:
        return None  # unknown notification: ignore
    return error(-32601, f"method not found: {method}")


def serve(stdin: TextIO | None = None, stdout: TextIO | None = None) -> None:
    """Newline-delimited JSON-RPC loop (the MCP stdio transport)."""
    fin = stdin or sys.stdin
    fout = stdout or sys.stdout
    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle_message(msg)
        if response is not None:
            fout.write(json.dumps(response, ensure_ascii=False) + "\n")
            fout.flush()


if __name__ == "__main__":
    serve()
