"""Ledger: hash chain, tamper evidence, windows, Merkle, HKDF/PRF."""

import tempfile
import unittest
from pathlib import Path

from gist_engine import crypto as C
from gist_engine.ledger import Ledger, LedgerError, TraceWindow


class TestChain(unittest.TestCase):
    def test_chain_and_verify(self):
        led = Ledger()
        led.append("a", {"x": 1})
        led.append("b", {"y": [1, 2]})
        led.append("a", {"x": 2})
        self.assertTrue(led.verify_chain())
        self.assertEqual(len(led), 3)

    def test_tamper_detected(self):
        led = Ledger()
        led.append("a", {"x": 1})
        led.append("b", {"y": 2})
        led.entries[0].payload["x"] = 999
        self.assertFalse(led.verify_chain())

    def test_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ledger.jsonl"
            led = Ledger(path=p)
            led.append("a", {"x": 1})
            led.append("b", {"y": 2})
            head = led.head_hash
            loaded = Ledger.load(p)
            self.assertEqual(loaded.head_hash, head)
            self.assertTrue(loaded.verify_chain())

    def test_corrupted_file_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ledger.jsonl"
            led = Ledger(path=p)
            led.append("a", {"x": 1})
            text = p.read_text().replace('"x": 1', '"x": 7').replace('"x":1', '"x":7')
            p.write_text(text)
            with self.assertRaises(LedgerError):
                Ledger.load(p)

    def test_wallclock_meta_outside_hash(self):
        """Two ledgers with identical payloads but different clocks have equal hashes."""
        l1 = Ledger(clock=lambda: 1.0)
        l2 = Ledger(clock=lambda: 999.0)
        for led in (l1, l2):
            led.append("a", {"x": 1})
            led.append("b", {"y": 2})
        self.assertEqual(l1.head_hash, l2.head_hash)


class TestWindow(unittest.TestCase):
    def test_window_projection_and_local_counter(self):
        led = Ledger()
        led.append("slot_commit", {"slot": 3, "word": "0+-"})
        led.append("slot_commit", {"slot": 5, "word": "+--"})
        led.append("gate_eval", {"cycle": 1})
        led.append("slot_commit", {"slot": 3, "word": "0+-"})
        w3 = TraceWindow(name="w3", kinds=("slot_commit",), scope_slots=(3,))
        wall = TraceWindow(name="wall")
        self.assertEqual(w3.local_counter(led), 2)
        self.assertEqual(wall.local_counter(led), 4)
        # windows are causal: bounded span cannot see later entries
        w_bounded = TraceWindow(name="wb", seq1=2)
        self.assertEqual(w_bounded.local_counter(led), 2)

    def test_passive_projection_does_not_mutate(self):
        led = Ledger()
        led.append("a", {"x": 1})
        before = [e.to_json() for e in led]
        TraceWindow(name="w").project(led)
        after = [e.to_json() for e in led]
        self.assertEqual(before, after)


class TestCrypto(unittest.TestCase):
    def test_merkle_root_changes_on_any_leaf(self):
        leaves = [C.merkle_leaf({"slot": i}) for i in range(64)]
        root = C.merkle_root(leaves)
        leaves2 = list(leaves)
        leaves2[17] = C.merkle_leaf({"slot": 17, "tampered": True})
        self.assertNotEqual(root, C.merkle_root(leaves2))
        # 64 leaves -> 7 levels (64,32,16,8,4,2,1)
        self.assertEqual([len(lv) for lv in C.merkle_levels(leaves)],
                         [64, 32, 16, 8, 4, 2, 1])

    def test_hkdf_prf_stamp_determinism_and_binding(self):
        k1 = C.session_key("what causes X?", "abc123")
        k2 = C.session_key("what causes X?", "abc123")
        k3 = C.session_key("what causes Y?", "abc123")
        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)
        stamp1 = C.decision_stamp(k1, "r" * 64, ["a" * 64], "101101", "h" * 64)
        stamp2 = C.decision_stamp(k1, "r" * 64, ["a" * 64], "101101", "h" * 64)
        stamp3 = C.decision_stamp(k3, "r" * 64, ["a" * 64], "101101", "h" * 64)
        self.assertEqual(stamp1, stamp2)
        self.assertNotEqual(stamp1, stamp3)  # bound to the prompt

    def test_hkdf_rfc5869_shape(self):
        out = C.hkdf(b"ikm", b"salt", b"info", length=64)
        self.assertEqual(len(out), 64)


if __name__ == "__main__":
    unittest.main()
