"""The do-operator refinement tests: T1 (random-SCM ground truth),
T2 (canonical Pearl fixtures), T3 (rule soundness) from
PROPOSAL_DO_OPERATOR.md, plus Field.do surgery.

Bars are the signed acceptance criteria: identified estimands must match
ground truth EXACTLY (enumeration vs enumeration, 1e-9 float slack);
refusals must be honest; rule applications must never change the query's
value.
"""

import math
import unittest
from itertools import product

from gist_engine import causal as C
from gist_engine.field import Cell, Channel, Field, Module

N_T1_SCMS = 60          # random SCMs in the suite (each with 12 queries)
TOL = 1e-9


class TestT1RandomGroundTruth(unittest.TestCase):
    def test_identified_estimands_match_ground_truth_exactly(self):
        """Every identified P(Y|do(X)) either equals oracle surgery exactly
        (when the positivity/overlap assumption holds) or refuses estimation
        with the violating strata attributed. Refusals of identification are
        likewise attributed. 100% bars, per the signed protocol."""
        exact = 0
        positivity_refusals = 0
        refused = 0
        for seed in range(N_T1_SCMS):
            scm = C.random_scm(seed, n_observed=4)
            obs = scm.observed
            for x_var, y_var in product(obs, obs):
                if x_var == y_var:
                    continue
                result = C.identify(scm, x_var, y_var)
                if isinstance(result, C.NotIdentifiable):
                    refused += 1
                    self.assertTrue(result.reason)
                    self.assertTrue(result.ask)
                    continue
                for x in C.TRITS:
                    violations = result.positivity_violations(scm, x)
                    if violations:
                        positivity_refusals += 1
                        # the refusal must be real: each attributed stratum
                        # genuinely carries zero observational mass
                        for stratum in violations:
                            self.assertEqual(scm.prob(stratum), 0.0)
                        with self.assertRaises(C.PositivityError):
                            result.evaluate(scm, x, 1)
                        continue
                    for y in C.TRITS:
                        est = result.evaluate(scm, x, y)
                        truth = C.ground_truth_do(scm, x_var, x, y_var, y)
                        self.assertAlmostEqual(
                            est, truth, delta=TOL,
                            msg=(f"seed={seed} {result.query} tier="
                                 f"{result.tier} Z={result.adjustment} "
                                 f"x={x} y={y}"),
                        )
                        exact += 1
        # the suite must actually exercise all three outcomes
        self.assertGreater(exact, 300)
        self.assertGreater(positivity_refusals, 5)
        self.assertGreater(refused, 10)

    def test_interventional_distributions_are_distributions(self):
        for seed in range(8):
            scm = C.random_scm(seed, n_observed=4)
            x_var, y_var = scm.observed[0], scm.observed[-1]
            for x in C.TRITS:
                total = sum(
                    C.ground_truth_do(scm, x_var, x, y_var, y)
                    for y in C.TRITS
                )
                self.assertAlmostEqual(total, 1.0, delta=TOL)

    def test_counterfactual_consistency_axiom(self):
        """Consistency: if X=x actually, then Y_{X=x} = Y (per world)."""
        for seed in range(10):
            scm = C.random_scm(seed, n_observed=4)
            x_var, y_var = scm.observed[0], scm.observed[-1]
            for x in C.TRITS:
                for y in C.TRITS:
                    p_evidence = scm.prob({x_var: x, y_var: y})
                    if p_evidence < 1e-12:
                        continue
                    r = C.counterfactual(
                        scm,
                        evidence={x_var: x, y_var: y},
                        do={x_var: x},
                        query={y_var: y},
                    )
                    self.assertAlmostEqual(r.probability, 1.0, delta=TOL)

    def test_pn_ps_pns_in_range_ternary(self):
        """PN/PS/PNS are exact probabilities on the ternary family."""
        checked = 0
        for seed in range(20):
            scm = C.random_scm(seed, n_observed=4)
            x_var, y_var = scm.observed[0], scm.observed[-1]
            if scm.prob({x_var: 1, y_var: 1}) < 1e-9:
                continue
            for v in (C.pn(scm, x_var, y_var), C.ps(scm, x_var, y_var),
                      C.pns(scm, x_var, y_var)):
                self.assertGreaterEqual(v, -TOL)
                self.assertLessEqual(v, 1.0 + TOL)
            checked += 1
        self.assertGreater(checked, 5)

    def test_pn_inside_tian_pearl_bounds_binary(self):
        """On the binary sub-family (the bounds' native setting), the exact
        twin-network PN always lies inside the Tian-Pearl bounds computed
        from distributions alone."""
        checked = 0
        for seed in range(24):
            scm = C.random_binary_scm(seed, n_observed=4)
            x_var, y_var = scm.observed[0], scm.observed[-1]
            p_xy = scm.prob({x_var: 1, y_var: 1})
            if p_xy < 1e-9:
                continue
            pn_exact = C.pn(scm, x_var, y_var, x=1, y=1, x_alt=-1)
            p_y_do_alt = C.ground_truth_do(scm, x_var, -1, y_var, 1)
            lo, hi = C.pn_bounds(
                p_y=scm.prob({y_var: 1}),
                p_xy=p_xy,
                p_y_do_alt=p_y_do_alt,
                p_ny_do_alt=1.0 - p_y_do_alt,
                p_nx_ny=scm.prob({x_var: -1, y_var: -1}),
            )
            self.assertGreaterEqual(pn_exact, lo - 1e-9,
                                    msg=f"seed={seed} pn={pn_exact} lo={lo}")
            self.assertLessEqual(pn_exact, hi + 1e-9,
                                 msg=f"seed={seed} pn={pn_exact} hi={hi}")
            checked += 1
        self.assertGreater(checked, 10)


class TestT2CanonicalFixtures(unittest.TestCase):
    def _positivity_aware_exactness(self, scm, result):
        """Assert exact match on positivity-clean treatment values and
        attributed refusal on the rest; return the clean values."""
        clean = []
        for x in C.TRITS:
            violations = result.positivity_violations(scm, x)
            if violations:
                for stratum in violations:
                    self.assertEqual(scm.prob(stratum), 0.0)
                with self.assertRaises(C.PositivityError):
                    result.evaluate(scm, x, 1)
                continue
            clean.append(x)
            for y in C.TRITS:
                self.assertAlmostEqual(
                    result.evaluate(scm, x, y),
                    C.ground_truth_do(scm, "X", x, "Y", y),
                    delta=TOL,
                )
        self.assertTrue(clean, "no positivity-clean treatment value")
        return clean

    def test_frontdoor_smoking_tar_cancer(self):
        scm = C.frontdoor_fixture()
        result = C.identify(scm, "X", "Y")
        self.assertIsInstance(result, C.Estimand)
        self.assertEqual(result.tier, "frontdoor")
        self.assertEqual(result.adjustment, ("M",))
        self._positivity_aware_exactness(scm, result)
        # the fixture is causally live: do(X) moves M and Y
        self.assertGreater(
            abs(C.ground_truth_do(scm, "X", 1, "Y", 1)
                - C.ground_truth_do(scm, "X", -1, "Y", 1)),
            0.05,
        )

    def test_backdoor_adjustment_and_simpson_gap(self):
        scm = C.backdoor_fixture()
        result = C.identify(scm, "X", "Y")
        self.assertIsInstance(result, C.Estimand)
        self.assertEqual(result.tier, "backdoor")
        self.assertIn("Z", result.adjustment)
        clean = self._positivity_aware_exactness(scm, result)
        # Simpson-style gap at a positivity-clean treatment value: the
        # naive conditional differs from the interventional truth (the
        # confounder is doing real work)
        gaps = [
            abs(scm.prob({"Y": 1}, given={"X": x})
                - C.ground_truth_do(scm, "X", x, "Y", 1))
            for x in clean
        ]
        self.assertGreater(max(gaps), 0.01, f"gaps={gaps} at clean={clean}")

    def test_bow_graph_refuses(self):
        scm = C.bow_fixture()
        result = C.identify(scm, "X", "Y")
        self.assertIsInstance(result, C.NotIdentifiable)
        self.assertIn("instrument", result.ask)

    def test_estimand_derivations_recorded(self):
        result = C.identify(C.frontdoor_fixture(), "X", "Y")
        self.assertTrue(result.derivation)
        self.assertTrue(any("frontdoor" in step for step in result.derivation))


class TestT3RuleSoundness(unittest.TestCase):
    """A licensed do-calculus rule application never changes the value."""

    def test_rule1_observation_deletion_sound(self):
        checked = 0
        for seed in range(24):
            scm = C.random_scm(seed, n_observed=4)
            obs = scm.observed
            for y, z, x in product(obs, obs, obs):
                if len({y, z, x}) < 3:
                    continue
                if not C.rule1_deletes_observation(scm, y, z, {x}):
                    continue
                mut = scm.do({x: 1})
                for yv in C.TRITS:
                    rhs = mut.prob({y: yv})
                    for zv in C.TRITS:
                        if mut.prob({z: zv}) < 1e-12:
                            continue  # undefined conditional stratum
                        lhs = mut.prob({y: yv}, given={z: zv})
                        self.assertAlmostEqual(
                            lhs, rhs, delta=1e-7,
                            msg=f"rule1 seed={seed} y={y} z={z} do({x})",
                        )
                checked += 1
        self.assertGreater(checked, 20)

    def test_rule2_action_observation_exchange_sound(self):
        checked = 0
        for seed in range(24):
            scm = C.random_scm(seed, n_observed=4)
            obs = scm.observed
            for y, z in product(obs, obs):
                if y == z:
                    continue
                if not C.rule2_exchange_action_observation(scm, y, z, set()):
                    continue
                for zv in C.TRITS:
                    p_z = scm.prob({z: zv})
                    if p_z < 1e-9:
                        continue
                    for yv in C.TRITS:
                        lhs = scm.do({z: zv}).prob({y: yv})
                        rhs = scm.prob({y: yv}, given={z: zv})
                        self.assertAlmostEqual(
                            lhs, rhs, delta=1e-7,
                            msg=f"rule2 seed={seed} P({y}|do({z}={zv}))",
                        )
                checked += 1
        self.assertGreater(checked, 10)

    def test_rule3_action_deletion_sound(self):
        checked = 0
        for seed in range(24):
            scm = C.random_scm(seed, n_observed=4)
            obs = scm.observed
            for y, z in product(obs, obs):
                if y == z:
                    continue
                if not C.rule3_deletes_action(scm, y, z, set()):
                    continue
                for zv in C.TRITS:
                    for yv in C.TRITS:
                        lhs = scm.do({z: zv}).prob({y: yv})
                        rhs = scm.prob({y: yv})
                        self.assertAlmostEqual(
                            lhs, rhs, delta=1e-7,
                            msg=f"rule3 seed={seed} P({y}|do({z}={zv}))",
                        )
                checked += 1
        self.assertGreater(checked, 10)

    def test_d_separation_implies_independence(self):
        """Global Markov property on the generated family."""
        checked = 0
        for seed in range(16):
            scm = C.random_scm(seed, n_observed=4)
            obs = scm.observed
            for a, b in product(obs, obs):
                if a == b:
                    continue
                if not C.d_separated(scm, {a}, {b}, set()):
                    continue
                for av in C.TRITS:
                    pa = scm.prob({a: av})
                    if pa < 1e-9:
                        continue
                    for bv in C.TRITS:
                        joint = scm.prob({a: av, b: bv})
                        self.assertAlmostEqual(
                            joint, pa * scm.prob({b: bv}), delta=1e-7,
                            msg=f"markov seed={seed} {a}⊥{b}",
                        )
                checked += 1
        self.assertGreater(checked, 5)


class TestFieldSurgery(unittest.TestCase):
    def _field(self) -> Field:
        f = Field(name="surgery", deadband=0.5, amp_relax=0.8)
        f.add_module(Module(name="x", cells=[Cell(theta=0.4, amp=1.0)]))
        f.add_module(Module(name="y", cells=[Cell(theta=math.pi / 2, amp=0.5)]))
        f.add_module(Module(name="z", cells=[Cell(theta=0.2, amp=1.0)]))
        f.add_channel(Channel(src="z:0", dst="x:0", weight=0.6))
        f.add_channel(Channel(src="x:0", dst="y:0", weight=0.6))
        return f

    def test_do_severs_and_pins(self):
        f = self._field()
        twin = f.do({"x": -1})
        # inbound to x severed; x -> y kept
        dsts = {ch.dst.split(":")[0] for ch in twin.channels}
        self.assertNotIn("x", dsts)
        self.assertIn("y", dsts)
        # x pinned at the - pole and latched
        self.assertAlmostEqual(twin.modules["x"].cells[0].theta, math.pi)
        self.assertEqual(twin.modules["x"].cells[0].sigma, -1)
        # original untouched
        self.assertAlmostEqual(f.modules["x"].cells[0].theta, 0.4)

    def test_intervention_holds_under_flow_and_propagates(self):
        f = self._field()
        twin = f.do({"x": -1})
        twin.flow(4.0)
        # the pinned module is a fixed point
        self.assertAlmostEqual(twin.modules["x"].cells[0].theta, math.pi,
                               places=9)
        # and downstream y turned toward the intervened pole
        y_theta = twin.modules["y"].cells[0].theta
        self.assertGreater(abs(y_theta), 2.0)  # heading to π, not 0

    def test_do_rejects_bad_input(self):
        f = self._field()
        with self.assertRaises(KeyError):
            f.do({"nope": 1})
        with self.assertRaises(ValueError):
            f.do({"x": 2})


if __name__ == "__main__":
    unittest.main()
