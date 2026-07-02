"""Variant A: the ternary verdict bridge - tool call, MCP surface, stitch."""

import io
import json
import unittest

from gist_engine.mcp_server import handle_message, serve, tool_definitions
from gist_engine.verdict import TOOL_SPEC, as_tool_call, verdict


def supporting_atoms(scope=(0, 0, 0)):
    return [
        {"content": "all 74 unit tests pass after the change",
         "polarity": 0.92, "salience": 0.9, "address": list(scope)},
        {"content": "behavior snapshots match golden files",
         "polarity": 0.88, "salience": 0.85, "address": list(scope)},
        {"content": "one reviewer notes a minor style regression",
         "polarity": -0.4, "salience": 0.3, "address": list(scope)},
    ]


def contradicting_atoms(scope=(0, 0, 0)):
    return [
        {"content": "integration suite fails on the new path",
         "polarity": -0.9, "salience": 0.95, "address": list(scope)},
        {"content": "latency regression of 40% under load",
         "polarity": -0.85, "salience": 0.9, "address": list(scope)},
        {"content": "one synthetic micro-benchmark improved",
         "polarity": 0.35, "salience": 0.25, "address": list(scope)},
    ]


class TestVerdict(unittest.TestCase):
    def test_yes_on_decisive_support(self):
        v = verdict("the refactor preserves behavior",
                    atoms=supporting_atoms(), session_id="v-yes")
        self.assertEqual(v.decision, "yes")
        self.assertEqual(v.trit, 1)
        self.assertGreater(v.confidence, 0.3)
        self.assertIn(v.basis, ("gated-release", "board-read"))
        self.assertTrue(v.why)

    def test_no_on_decisive_contradiction(self):
        v = verdict("the refactor preserves behavior",
                    atoms=contradicting_atoms(), session_id="v-no")
        self.assertEqual(v.decision, "no")
        self.assertEqual(v.trit, -1)

    def test_maybe_on_no_evidence_with_asks(self):
        v = verdict("an unexamined claim", atoms=[], session_id="v-maybe")
        self.assertEqual(v.decision, "maybe")
        self.assertEqual(v.trit, 0)
        self.assertLessEqual(v.confidence, 0.5)

    def test_maybe_on_contested_evidence(self):
        atoms = [
            {"content": "strong support", "polarity": 0.9, "salience": 0.9,
             "address": [0, 0, 0]},
            {"content": "strong contradiction", "polarity": -0.9,
             "salience": 0.88, "address": [0, 0, 0]},
        ]
        v = verdict("a contested claim", atoms=atoms, session_id="v-cont")
        self.assertEqual(v.decision, "maybe")
        self.assertTrue(v.asks or v.holds)

    def test_deterministic(self):
        v1 = verdict("claim", atoms=supporting_atoms(), session_id="v-det")
        v2 = verdict("claim", atoms=supporting_atoms(), session_id="v-det")
        self.assertEqual(v1.to_json(), v2.to_json())

    def test_tool_call_roundtrip(self):
        args = json.dumps({"claim": "the refactor preserves behavior",
                           "atoms": supporting_atoms()})
        out = json.loads(as_tool_call(args))
        self.assertEqual(out["decision"], "yes")
        self.assertIn("asks", out)
        # the spec is a valid tool definition shape
        self.assertEqual(TOOL_SPEC["name"], "gist_verdict")
        self.assertIn("input_schema", TOOL_SPEC)
        self.assertIn("claim", TOOL_SPEC["input_schema"]["properties"])


class TestMCPServer(unittest.TestCase):
    def rpc(self, method, params=None, msg_id=1):
        return handle_message({"jsonrpc": "2.0", "id": msg_id,
                               "method": method, "params": params or {}})

    def test_initialize_and_list(self):
        init = self.rpc("initialize")
        self.assertEqual(init["result"]["serverInfo"]["name"], "gist-engine")
        self.assertIn("tools", init["result"]["capabilities"])
        tools = self.rpc("tools/list")["result"]["tools"]
        names = {t["name"] for t in tools}
        self.assertIn("gist_verdict", names)
        self.assertIn("gist_open", names)
        self.assertIn("gist_verify", names)
        for t in tools:
            self.assertIn("inputSchema", t)

    def test_verdict_tool_call(self):
        resp = self.rpc("tools/call", {
            "name": "gist_verdict",
            "arguments": {"claim": "the refactor preserves behavior",
                          "atoms": supporting_atoms()},
        })
        self.assertFalse(resp["result"]["isError"])
        payload = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(payload["decision"], "yes")

    def test_session_lifecycle_over_mcp(self):
        opened = self.rpc("tools/call", {
            "name": "gist_open",
            "arguments": {"prompt": "session over mcp",
                          "gate_scope": "occupied"},
        })
        sid = json.loads(opened["result"]["content"][0]["text"])["session_id"]
        self.rpc("tools/call", {
            "name": "gist_ingest",
            "arguments": {"session_id": sid, "atoms": supporting_atoms()},
        })
        self.rpc("tools/call", {
            "name": "gist_step", "arguments": {"session_id": sid, "n": 3},
        })
        state = json.loads(
            self.rpc("tools/call", {
                "name": "gist_state", "arguments": {"session_id": sid},
            })["result"]["content"][0]["text"]
        )
        self.assertEqual(len(state["board"]), 64)
        self.assertGreater(state["S"], 0.5)

    def test_unknown_tool_is_tool_error_not_protocol_error(self):
        resp = self.rpc("tools/call", {"name": "nope", "arguments": {}})
        self.assertTrue(resp["result"]["isError"])

    def test_serve_loop_stdio(self):
        lines = [
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                        "params": {}}),
            json.dumps({"jsonrpc": "2.0", "method":
                        "notifications/initialized"}),
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
        ]
        fin = io.StringIO("\n".join(lines) + "\n")
        fout = io.StringIO()
        serve(fin, fout)
        responses = [json.loads(l) for l in fout.getvalue().splitlines()]
        self.assertEqual(len(responses), 2)  # notification produced none
        self.assertEqual(responses[0]["id"], 1)
        self.assertEqual(responses[1]["id"], 2)


if __name__ == "__main__":
    unittest.main()
