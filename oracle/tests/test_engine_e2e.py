"""End-to-end: the full GIST pipeline, deterministic and replay-verified."""

import tempfile
import unittest
from pathlib import Path

from gist_engine import Atom, GistConfig, GistEngine, verify_ledger
from gist_engine.democorpus import PROMPT, build_corpus, drive
from gist_engine.crypto import decision_stamp, merkle_root, session_key
from gist_engine.walks import TIER_ORDER


def run_session(ledger_path=None):
    engine = GistEngine(prompt=PROMPT, session_id="e2e-fixed",
                        ledger_path=ledger_path)
    initial, reserve = build_corpus()
    engine.ingest(initial)
    release = drive(engine, reserve)
    return engine, release


class TestEndToEnd(unittest.TestCase):
    def test_full_pipeline_reaches_stamped_release(self):
        engine, release = run_session()
        self.assertIsNotNone(release, engine.gate_report and
                             engine.gate_report.to_json())
        # release integrity
        self.assertIn(release["tier"], TIER_ORDER)
        self.assertEqual(len(release["stamp"]), 64)
        self.assertEqual(len(release["leaf_root"]), 64)
        self.assertTrue(release["coordinate"]["dyadic"])
        # gate: all seven checks passed
        self.assertTrue(release["gate"]["eligible"])
        self.assertEqual(len(release["gate"]["checks"]), 7)
        self.assertTrue(all(c["passed"] for c in release["gate"]["checks"]))

    def test_agentic_loop_intents_emitted_and_fulfilled(self):
        engine, release = run_session()
        kinds = [e.kind for e in engine.ledger]
        self.assertIn("retrieval_intent", kinds)
        self.assertIn("intent_fulfilled", kinds)
        self.assertIn("slot_saturated", kinds)
        self.assertIn("gate_proposal", kinds)
        self.assertIn("ladder_round", kinds)
        self.assertIn("reconciliation", kinds)
        self.assertIn("decision_stamp", kinds)
        self.assertIn("release", kinds)
        # six ladder rounds
        self.assertEqual(len([k for k in kinds if k == "ladder_round"]), 6)

    def test_stamp_recomputable_from_ledger(self):
        """A third party recomputes the stamp from public ledger content."""
        engine, release = run_session()
        stamp_entry = engine.ledger.last_of_kind("decision_stamp")
        init_entry = engine.ledger.last_of_kind("session_init")
        p = stamp_entry.payload
        key = session_key(init_entry.payload["prompt"],
                          init_entry.payload["session_id"])
        recomputed = decision_stamp(
            key=key,
            leaf_root=p["leaf_root"],
            round_roots=p["round_roots"],
            decision_coordinate=p["coordinate"]["dyadic"],
            head_hash=p["head_at_stamp"],
        )
        self.assertEqual(recomputed, p["stamp"])
        self.assertEqual(release["stamp"], p["stamp"])

    def test_determinism_two_runs_identical(self):
        e1, r1 = run_session()
        e2, r2 = run_session()
        self.assertEqual(r1["stamp"], r2["stamp"])
        s1 = [(e.kind, e.payload) for e in e1.ledger]
        s2 = [(e.kind, e.payload) for e in e2.ledger]
        self.assertEqual(s1, s2)
        self.assertEqual(e1.ledger.head_hash, e2.ledger.head_hash)

    def test_replay_verification_from_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "session.jsonl"
            engine, release = run_session(ledger_path=path)
            self.assertIsNotNone(release)
            report = verify_ledger(path)
            self.assertTrue(report["chain_ok"])
            self.assertTrue(report["verified"], report["mismatches"])
            self.assertEqual(report["head_recorded"], report["head_replayed"])

    def test_tampered_ledger_fails_verification(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "session.jsonl"
            run_session(ledger_path=path)
            text = path.read_text()
            tampered = text.replace('"polarity": 0.92', '"polarity": -0.92', 1)
            self.assertNotEqual(text, tampered)
            path.write_text(tampered)
            report = verify_ledger(path)
            self.assertFalse(report["verified"])

    def test_state_json_board_shape(self):
        engine, _ = run_session()
        state = engine.state_json()
        self.assertEqual(len(state["board"]), 64)
        self.assertEqual(state["ledger_length"], len(engine.ledger))
        contributing = [b for b in state["board"] if b["atoms"] > 0]
        self.assertGreaterEqual(len(contributing), 8)
        for b in contributing:
            self.assertIn("metrics", b)
            self.assertIn(b["tier"], TIER_ORDER)
        self.assertIsNotNone(state["release"])
        self.assertIsNotNone(state["ladder"])

    def test_viability_lifecycle(self):
        engine = GistEngine(prompt=PROMPT, session_id="viab")
        v0 = engine.viability()
        self.assertEqual(v0["mode"], "intentional")
        initial, reserve = build_corpus()
        engine.ingest(initial)
        self.assertEqual(engine.viability()["mode"], "reactive")
        drive(engine, reserve)
        self.assertEqual(engine.viability()["mode"], "passive")
        self.assertTrue(engine.viability()["released"])

    def test_unaddressed_atoms_hash_project_deterministically(self):
        e1 = GistEngine(prompt="p", session_id="h1")
        e2 = GistEngine(prompt="p", session_id="h2")
        a = Atom(content="an unaddressed observation")
        p1 = e1.ingest(a)[0]
        p2 = e2.ingest(a)[0]
        self.assertEqual((p1.slot, p1.polarity, p1.salience),
                         (p2.slot, p2.polarity, p2.salience))

    def test_vdr_hint_on_contested_scope(self):
        """Balance-violating candidate words surface exact VDR attribution."""
        cfg = GistConfig()
        engine = GistEngine(prompt="contested", session_id="vdr", config=cfg)
        scope = (1, 2, 0)
        atoms = [
            Atom(content="strong opposing lead", polarity=-0.95, salience=0.95,
                 address=scope),
            Atom(content="weak support trailing", polarity=0.85, salience=0.30,
                 address=scope),
        ]
        engine.ingest(atoms)
        for _ in range(3):
            engine.step()
        kinds = [e.kind for e in engine.ledger]
        commits = [e.payload for e in engine.ledger.of_kind("slot_commit")]
        held = [c for c in commits if c["reason"] == "balance-violation"]
        self.assertTrue(held, commits)
        self.assertIn("vdr_hint", kinds)
        hint = engine.ledger.of_kind("vdr_hint")[0].payload
        self.assertEqual(hint["action"], "seek_counter_evidence")
        self.assertEqual(hint["cell"], held[0]["violation_cell"])


if __name__ == "__main__":
    unittest.main()
