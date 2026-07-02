"""GIST-NN: equivalence proofs - the functional form loses nothing.

The network is constructed analytically from a live field (no training) and
must compute the same reduction as the reference engine: flow trajectories,
beliefs, quantization, and barrier - state for state, over the full 64-slot
lattice with real evidence in it.
"""

import unittest

from gist_engine import GistEngine
from gist_engine.democorpus import PROMPT, build_corpus
from gist_engine.field import Cell, Channel, Field, Module
from gist_engine.neural import GistNeural

PLACES = 9  # double-precision agreement between algebraically equal paths


def loaded_engine():
    eng = GistEngine(prompt=PROMPT, session_id="nn-src")
    initial, _reserve = build_corpus()
    eng.ingest(initial)
    eng.step()  # absorb atoms so the lattice carries real structure
    return eng


class TestEquivalence(unittest.TestCase):
    def assert_states_match(self, field: Field, nn: GistNeural):
        i = 0
        for name, m in field.modules.items():
            for cell in m.cells:
                self.assertAlmostEqual(cell.theta, nn.theta[i], places=PLACES,
                                       msg=f"theta {name}[{i}]")
                self.assertAlmostEqual(cell.amp, nn.amp[i], places=PLACES,
                                       msg=f"amp {name}[{i}]")
                i += 1
        for j, name in enumerate(nn.w.modules):
            self.assertAlmostEqual(field.modules[name].belief, nn.belief[j],
                                   places=PLACES, msg=f"belief {name}")

    def test_flow_equivalence_full_lattice(self):
        eng = loaded_engine()
        nn = GistNeural.from_field(eng.field)
        self.assert_states_match(eng.field, nn)  # identical start
        eng.field.flow(2.0)
        nn.flow(2.0)
        self.assert_states_match(eng.field, nn)

    def test_multi_cycle_trajectory_equivalence(self):
        eng = loaded_engine()
        nn = GistNeural.from_field(eng.field)
        for _ in range(5):
            eng.field.flow(1.0)
            nn.flow(1.0)
        self.assert_states_match(eng.field, nn)

    def test_quantization_equivalence(self):
        eng = loaded_engine()
        eng.field.flow(2.0)
        nn = GistNeural.from_field(eng.field)
        trits_nn = nn.quantize()
        i = 0
        for name, m in eng.field.modules.items():
            for t in m.trits(eng.field.deadband):
                self.assertEqual(t, trits_nn[i], f"trit {name}[{i}]")
                i += 1

    def test_commit_head_barrier_equivalence(self):
        """The native holdcase scenario through the NN head."""
        import math
        f = Field(name="parity", dt=0.125, gain=1.0, deadband=0.5)
        f.add_module(Module(name="holdcase", cells=[
            Cell(theta=math.pi), Cell(theta=0.0), Cell(theta=math.pi / 2)]))
        nn = GistNeural.from_field(f)
        head = nn.commit_head("holdcase")
        self.assertEqual(head["trits"], [-1, 1, 0])
        self.assertFalse(head["admissible"])
        self.assertEqual(head["violation_cell"], 0)
        r = f.commit("holdcase")
        self.assertEqual(list(r.trits), head["trits"])
        self.assertEqual(r.violation_cell, head["violation_cell"])

    def test_angular_channel_rotation_block(self):
        """A nonzero-angle channel = an SO(2) weight block, exactly."""
        import math
        f = Field(name="rot", dt=0.125, gain=1.0, deadband=0.5)
        f.add_module(Module(name="m", cells=[Cell(theta=0.3, amp=1.2),
                                             Cell(theta=0.0, amp=1.0)]))
        f.add_channel(Channel(src="m:0", dst="m:1", weight=0.4,
                              angle=0.7))
        nn = GistNeural.from_field(f)
        f.flow(1.0)
        nn.flow(1.0)
        self.assertAlmostEqual(f.modules["m"].cells[1].theta, nn.theta[1],
                               places=PLACES)

    def test_weight_export_roundtrip(self):
        eng = loaded_engine()
        nn = GistNeural.from_field(eng.field)
        payload = nn.dumps()
        nn2 = GistNeural.loads(payload)
        nn.flow(1.5)
        nn2.flow(1.5)
        for a, b in zip(nn.theta, nn2.theta):
            self.assertAlmostEqual(a, b, places=12)
        for a, b in zip(nn.belief, nn2.belief):
            self.assertAlmostEqual(a, b, places=12)

    def test_dense_weight_matrices_shape(self):
        eng = loaded_engine()
        nn = GistNeural.from_field(eng.field)
        w_re, w_im = nn.w.dense()
        n = 64 * 6
        self.assertEqual(len(w_re), n)
        self.assertEqual(len(w_re[0]), n)
        # the lattice pyramid: 6 intra-slot edges per slot, angle 0 => W_im = 0
        nonzero = sum(1 for row in w_re for x in row if x != 0.0)
        self.assertEqual(nonzero, 64 * 6)
        self.assertTrue(all(x == 0.0 for row in w_im for x in row))

    def test_delayed_channels_rejected_explicitly(self):
        f = Field(name="d", dt=0.125)
        f.add_module(Module(name="m", cells=[Cell(), Cell()]))
        f.add_channel(Channel(src="m:0", dst="m:1", weight=0.5, delay=0.5))
        with self.assertRaises(ValueError):
            GistNeural.from_field(f)


if __name__ == "__main__":
    unittest.main()
