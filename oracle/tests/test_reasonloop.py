"""Variant B: the reasoning-chain stitcher (in-chain + pre-gate modes)."""

import unittest

from gist_engine.reasonloop import ReasonLoop, pre_gate


class TestInChain(unittest.TestCase):
    def test_chain_builds_toward_yes(self):
        loop = ReasonLoop(prompt="is the migration safe?", session_id="rl-1")
        fb = loop.feed("the schema change is backward compatible",
                       polarity=0.9, salience=0.85, address=(0, 0, 0))
        self.assertIn(fb.proceed, ("maybe", "yes"))
        loop.feed("rollback path tested and verified",
                  polarity=0.88, salience=0.8, address=(0, 0, 0))
        fb = loop.feed("a minor index rebuild is needed but non-blocking",
                       polarity=-0.3, salience=0.3, address=(0, 0, 0))
        self.assertGreater(fb.S, 0.5)
        v = loop.gate_answer()
        self.assertEqual(v.decision, "yes")
        self.assertEqual(v.trit, 1)

    def test_contradiction_surfaces_as_no_go(self):
        loop = ReasonLoop(prompt="is the migration safe?", session_id="rl-2")
        loop.feed("data loss observed in the staging run",
                  polarity=-0.95, salience=0.95, address=(1, 1, 1))
        fb = loop.feed("the feature flag looks nice though",
                       polarity=0.5, salience=0.2, address=(1, 1, 1))
        # dominant contradiction: the conclusion must not read yes
        self.assertIn(fb.proceed, ("no", "maybe"))
        v = loop.gate_answer()
        self.assertIn(v.decision, ("no", "maybe"))
        self.assertNotEqual(v.trit, 1)

    def test_steering_block_is_compact_and_live(self):
        loop = ReasonLoop(prompt="steering?", session_id="rl-3")
        loop.feed("first consideration supports the plan",
                  polarity=0.8, salience=0.7, address=(0, 1, 2))
        block = loop.steering_block()
        self.assertIn("[GIST field", block)
        self.assertIn("scope", block)
        self.assertLess(len(block), 1200)

    def test_exploratory_steps_hold_the_aperture_open(self):
        loop = ReasonLoop(prompt="open exploration", session_id="rl-4")
        fb = loop.feed("considering angle A", polarity=0.0, salience=0.5,
                       address=(2, 2, 2))
        self.assertEqual(fb.proceed, "maybe")
        self.assertEqual(fb.trit, 0)

    def test_deterministic_episode(self):
        def run():
            loop = ReasonLoop(prompt="det", session_id="rl-5")
            loop.feed("supporting step", polarity=0.9, salience=0.8,
                      address=(0, 0, 0))
            loop.feed("another supporting step", polarity=0.85, salience=0.8,
                      address=(0, 0, 1))
            return loop.gate_answer().to_json()
        self.assertEqual(run(), run())


class TestPreGate(unittest.TestCase):
    def test_pre_gate_passes_supported_answer(self):
        v = pre_gate(
            "the fix resolves the race condition",
            claims=[
                {"content": "the lock ordering is now consistent",
                 "polarity": 0.9, "salience": 0.9, "address": [0, 0, 0]},
                {"content": "stress test shows no recurrence in 10k runs",
                 "polarity": 0.92, "salience": 0.9, "address": [0, 0, 0]},
                {"content": "slight throughput cost measured",
                 "polarity": -0.35, "salience": 0.3, "address": [0, 0, 0]},
            ],
            session_id="pg-1",
        )
        self.assertEqual(v.decision, "yes")

    def test_pre_gate_maybe_without_stance(self):
        # hash-projected transcript: honest maybe (no manufactured verdicts)
        v = pre_gate("some unexamined instant answer\nwith two lines",
                     session_id="pg-2")
        self.assertIn(v.decision, ("maybe", "yes", "no"))
        self.assertEqual(v.basis, "board-read") if v.decision == "maybe" else None


if __name__ == "__main__":
    unittest.main()
