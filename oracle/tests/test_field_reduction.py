"""Field reduction semantics: parity with the CDC native runtime witnesses.

The scenarios and expected numbers here are copied from the CDC repository's
`native_reducer.cdc`, whose expectations the C native runtime executes and
verifies. Reproducing them exactly is the ground-truth check that this engine
implements the same calculus.
"""

import math
import unittest

from gist_engine.field import Cell, Channel, Field, Module

PI = math.pi
HALF_PI = math.pi / 2.0


def native_reducer_field() -> Field:
    """The exact field declared in native_reducer.cdc."""
    f = Field(name="reducer-field", dt=0.125, gain=1.0, deadband=0.5)
    council = Module(
        name="council",
        cells=[Cell(theta=HALF_PI), Cell(theta=0.0), Cell(theta=PI)],
        belief=0.0, prior=0.0, precision=1.0, action_gain=1.0,
    )
    child = Module(
        name="child",
        cells=[Cell(theta=0.0), Cell(theta=0.0), Cell(theta=HALF_PI)],
        belief=0.0, prior=0.0, precision=1.0, action_gain=1.0, parent="council",
    )
    holdcase = Module(
        name="holdcase",
        cells=[Cell(theta=PI), Cell(theta=0.0), Cell(theta=HALF_PI)],
        belief=0.0, prior=0.0, precision=1.0, action_gain=1.0,
    )
    f.add_module(council)
    f.add_module(child)
    f.add_module(holdcase)
    f.add_channel(Channel(src="council:0", dst="council:1",
                          weight=0.25, delay=0.0, angle=0.0))
    return f


class TestNativeReducerParity(unittest.TestCase):
    def test_flow_parity(self):
        """flow reducer-flow duration=1.0 expect-theta=council.b:0.25 tol 1e-6."""
        f = native_reducer_field()
        f.flow(1.0, frozen=True)
        self.assertAlmostEqual(f.modules["council"].cells[1].theta, 0.25, delta=1e-6)

    def test_commit_parity_accepted(self):
        """commit reducer-commit expect-trits=0+- expect-status=accepted reason=none."""
        f = native_reducer_field()
        result = f.commit("council")
        self.assertEqual(result.word, "0+-")
        self.assertEqual(result.status, "accepted")
        self.assertEqual(result.reason, "none")
        self.assertTrue(result.admissible)
        # T2 soundness: potential did not increase
        self.assertLessEqual(result.phi_after, result.phi_before + 1e-9)
        # latch: poles written
        self.assertEqual(f.modules["council"].latched_word(), (0, 1, -1))

    def test_commit_parity_held(self):
        """commit reducer-hold expect-trits=-+0 expect-status=held
        reason=balance-violation; no state mutation."""
        f = native_reducer_field()
        before = [c.theta for c in f.modules["holdcase"].cells]
        result = f.commit("holdcase")
        self.assertEqual(result.word, "-+0")
        self.assertEqual(result.status, "held")
        self.assertEqual(result.reason, "balance-violation")
        self.assertFalse(result.admissible)
        self.assertEqual(result.violation_cell, 0)
        after = [c.theta for c in f.modules["holdcase"].cells]
        self.assertEqual(before, after)
        self.assertEqual(f.modules["holdcase"].latched_word(), (0, 0, 0))

    def test_nest_parity(self):
        """nest reducer-nest expect-parent-belief=0.666667 expect-child-prior=0.666667."""
        f = native_reducer_field()
        parent_belief, child_prior = f.nest("council", "child")
        self.assertAlmostEqual(parent_belief, 2.0 / 3.0, delta=1e-6)
        self.assertAlmostEqual(child_prior, 2.0 / 3.0, delta=1e-6)

    def test_repair_mode_implements_prose_semantics(self):
        """barrier='repair' rotates the debt-forcing cell to its crossing."""
        f = native_reducer_field()
        result = f.commit("holdcase", barrier="repair")
        self.assertEqual(result.status, "accepted")
        self.assertIn(0, result.repaired_cells)
        # the repaired cell now sits at a crossing (trit 0, openness maximal)
        self.assertEqual(result.trits[0], 0)
        self.assertTrue(result.admissible)


class TestTraceAndSurfaceParity(unittest.TestCase):
    def test_trace_parity_with_native_surface(self):
        """native_surface.cdc: two modules at (0, π/2, π) trace to '+0-+0-'."""
        f = Field(name="surface-field", dt=0.125, gain=1.0, deadband=0.5)
        for name in ("surface-alpha", "surface-beta"):
            f.add_module(Module(name=name, cells=[
                Cell(theta=0.0), Cell(theta=HALF_PI), Cell(theta=PI),
            ]))
        trits = f.trace_trits(["surface-alpha", "surface-beta"])
        from gist_engine.walks import to_word
        self.assertEqual(to_word(trits), "+0-+0-")

    def test_passive_trace_does_not_mutate(self):
        f = native_reducer_field()
        snapshot = [(c.theta, c.amp, c.sigma) for m in f.modules.values() for c in m.cells]
        _ = f.trace_trits()
        after = [(c.theta, c.amp, c.sigma) for m in f.modules.values() for c in m.cells]
        self.assertEqual(snapshot, after)


class TestReductionLaws(unittest.TestCase):
    def test_flow_additivity(self):
        """T4: ⟶_{d1}; ⟶_{d2} = ⟶_{d1+d2} on the integration grid."""
        f1 = native_reducer_field()
        f2 = native_reducer_field()
        f1.flow(0.5)
        f1.flow(0.5)
        f2.flow(1.0)
        for m1, m2 in zip(f1.modules.values(), f2.modules.values()):
            for c1, c2 in zip(m1.cells, m2.cells):
                self.assertAlmostEqual(c1.theta, c2.theta, places=9)

    def test_local_confluence_disjoint_commits(self):
        """T3: commits of channel-disjoint modules commute."""
        def build() -> Field:
            f = Field(name="conf", deadband=0.5)
            f.add_module(Module(name="a", cells=[Cell(theta=0.0), Cell(theta=HALF_PI)]))
            f.add_module(Module(name="b", cells=[Cell(theta=0.2), Cell(theta=PI)]))
            return f

        f_ab, f_ba = build(), build()
        r1 = [f_ab.commit("a"), f_ab.commit("b")]
        r2 = [f_ba.commit("b"), f_ba.commit("a")]
        state_ab = [(c.theta, c.sigma) for m in f_ab.modules.values() for c in m.cells]
        state_ba = [(c.theta, c.sigma) for m in f_ba.modules.values() for c in m.cells]
        self.assertEqual(state_ab, state_ba)
        self.assertEqual({r.module: r.word for r in r1}, {r.module: r.word for r in r2})

    def test_deadband_jitter_plateau_signal(self):
        """Re-committing an unchanged word holds with deadband-jitter."""
        f = native_reducer_field()
        first = f.commit("council")
        self.assertEqual(first.status, "accepted")
        second = f.commit("council")
        self.assertEqual(second.status, "held")
        self.assertEqual(second.reason, "deadband-jitter")

    def test_commit_is_total(self):
        """Every commit either accepts (lower/equal Φ, admissible) or holds."""
        f = native_reducer_field()
        for name in list(f.modules):
            r = f.commit(name)
            self.assertIn(r.status, ("accepted", "held"))
            if r.accepted:
                self.assertTrue(r.admissible)
                self.assertLessEqual(r.phi_after, r.phi_before + 1e-9)


if __name__ == "__main__":
    unittest.main()
