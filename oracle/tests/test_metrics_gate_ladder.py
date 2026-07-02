"""Metrics, gate checks, and ladder reduction unit behavior."""

import math
import unittest

from gist_engine.algebra import coh, phase
from gist_engine.field import Cell, Channel, Field, Module
from gist_engine.gate import GateThresholds, evaluate_gate
from gist_engine.ladder import fuse_pair, run_ladder
from gist_engine.metrics import (
    SlotMetrics,
    causal_lift,
    cf_agreement,
    coverage,
    slot_coherence,
    slot_openness,
    stability,
)
from gist_engine.walks import from_word


def make_slot(name: str = "slot", read_amps=(1.8, 0.0, 0.6),
              read_thetas=(0.45, 0.0, 2.4)) -> Field:
    """A slot module with the corefold pyramid channels, like the engine's.

    Canonical dialectic fill: thesis cluster at read[0], antithesis at
    read[2] (the far end), the middle cell reserved for bridging evidence.
    """
    f = Field(name="t", deadband=0.5, amp_relax=0.8)
    cells = [Cell(theta=read_thetas[i], amp=read_amps[i]) for i in range(3)]
    # write cells begin at the crossing (engine convention: unformed = open)
    cells += [Cell(theta=math.pi / 2, amp=0.0) for _ in range(3)]
    f.add_module(Module(name=name, cells=cells))
    for src, dst in ((0, 3), (1, 3), (1, 5), (2, 5)):
        f.add_channel(Channel(src=f"{name}:{src}", dst=f"{name}:{dst}", weight=0.5))
    for src in (3, 5):
        f.add_channel(Channel(src=f"{name}:{src}", dst=f"{name}:4", weight=0.5))
    return f


class TestMetrics(unittest.TestCase):
    def test_coverage_monotone_saturating(self):
        self.assertEqual(coverage(0.0), 0.0)
        self.assertLess(coverage(1.0), coverage(3.0))
        self.assertLess(coverage(30.0), 1.0 + 1e-9)

    def test_pyramid_flow_then_metrics(self):
        f = make_slot()
        # from the crossing initialization the pyramid needs a few cycles'
        # worth of flow to converge on its fixpoint
        f.flow(6.0)
        m = f.modules["slot"]
        # write cone acquired amplitude and coherence from the pyramid
        self.assertGreater(m.cells[3].amp, 0.05)
        self.assertGreater(slot_coherence(m), 0.5)
        # dominant + cluster wins the singular (commit replaces the module
        # atomically, so re-fetch after committing)
        result = f.commit("slot")
        self.assertEqual(result.status, "accepted")
        self.assertEqual(f.modules["slot"].latched_word()[4], 1)

    def test_stability_decisive_vs_knife_edge(self):
        f = make_slot()
        f.flow(2.0)
        f.commit("slot")
        self.assertGreaterEqual(stability(f, "slot"), 0.75)
        # knife-edge: a barely-decisive cell at the deadband boundary is
        # jitter-fragile before commitment...
        edge_theta = math.acos(0.5) - 0.01
        g = make_slot(read_amps=(1.0, 0.0, 0.0),
                      read_thetas=(edge_theta, 0.0, 0.0))
        self.assertLess(stability(g, "slot"), 1.0)
        # ...and the commit snap hardens it (pole hysteresis, by design)
        g.flow(2.0)
        g.commit("slot")
        self.assertGreaterEqual(stability(g, "slot"), 0.75)

    def test_cf_survival_dominant_cluster_ceiling(self):
        """Dominant-cluster slots hit exactly the (n-1)/n = 2/3 ceiling."""
        f = make_slot()
        f.flow(2.0)
        f.commit("slot")
        a = cf_agreement(f, "slot")
        self.assertAlmostEqual(a, 2.0 / 3.0, places=6)

    def test_cf_survival_contested_is_lower(self):
        """Near-balanced opposing evidence is counterfactually fragile."""
        f = make_slot(read_amps=(1.0, 0.0, 0.98), read_thetas=(0.3, 0.0, 2.85))
        f.flow(2.0)
        f.commit("slot")
        self.assertLess(cf_agreement(f, "slot"), 0.67)

    def test_causal_lift_positive_for_coherent_evidence(self):
        f = make_slot()
        f.flow(2.0)
        f.commit("slot")
        self.assertGreater(causal_lift(f, "slot"), 0.3)

    def test_openness_split(self):
        # decisive + empty cells: aperture stays open (empty = maximally open)
        f = make_slot(read_amps=(1.8, 0.0, 0.0), read_thetas=(0.2, 0.0, 0.0))
        self.assertGreater(slot_openness(f.modules["slot"], 0.5), 0.6)
        # two decisive clusters + one empty: boundary nearly closed
        g = make_slot()
        self.assertLess(slot_openness(g.modules["slot"], 0.5), 0.35)


def metrics_for(slots, coh_=0.9, cov=0.8, u=0.9, a=2 / 3, lift=0.6, open_=0.2):
    return {
        s: SlotMetrics(slot=s, coherence=coh_, coverage=cov, stability=u,
                       cf_agreement=a, causal_lift=lift, openness=open_)
        for s in slots
    }


DIVERSE = [0, 21, 42, 63, 1, 11, 31, 47]
# addresses: (0,0,0),(1,1,1),(2,2,2),(3,3,3),(0,0,1),(0,2,3),(1,3,3),(2,3,3)


class TestGate(unittest.TestCase):
    def make_words(self, slots):
        return {s: from_word("+0-+0-") for s in slots} | {
            s: (0, 0, 0, 0, 0, 0) for s in range(64) if s not in slots
        }

    def test_gate_passes_with_diverse_saturated_slots(self):
        th = GateThresholds()
        report = evaluate_gate(
            slot_words=self.make_words(DIVERSE),
            slot_metrics=metrics_for(DIVERSE),
            saturated=set(DIVERSE),
            S_history=[0.9, 0.9, 0.9],
            thresholds=th,
        )
        self.assertTrue(report.eligible, [c.to_json() for c in report.checks])
        self.assertEqual(report.headline_tier, "localized")

    def test_gate_fails_coverage_and_parity(self):
        th = GateThresholds()
        slots = [0, 21]  # (0,0,0), (1,1,1): axes missing 2,3
        report = evaluate_gate(
            slot_words=self.make_words(slots),
            slot_metrics=metrics_for(slots),
            saturated=set(slots),
            S_history=[0.9, 0.9, 0.9],
            thresholds=th,
        )
        self.assertFalse(report.eligible)
        failed = {c.name for c in report.checks if not c.passed}
        self.assertIn("coverage", failed)

    def test_gate_hysteresis(self):
        th = GateThresholds()
        report = evaluate_gate(
            slot_words=self.make_words(DIVERSE),
            slot_metrics=metrics_for(DIVERSE),
            saturated=set(DIVERSE),
            S_history=[0.9, 0.4, 0.9],  # dipped inside the window
            thresholds=th,
        )
        failed = {c.name for c in report.checks if not c.passed}
        self.assertIn("global_agreement", failed)

    def test_gate_budget_release_flagged(self):
        th = GateThresholds()
        report = evaluate_gate(
            slot_words=self.make_words(DIVERSE),
            slot_metrics=metrics_for(DIVERSE),
            saturated=set(DIVERSE[:-1]),   # one slot never saturated
            S_history=[0.9, 0.9, 0.9],
            thresholds=th,
            budget_exhausted=True,
        )
        self.assertTrue(report.eligible)
        self.assertTrue(report.budget_release)


class TestLadder(unittest.TestCase):
    def _leaves(self):
        modules = {}
        hashes = {}
        for i in range(64):
            cells = [Cell(theta=0.4, amp=1.0 if i in DIVERSE else 0.0)
                     for _ in range(3)]
            cells += [Cell(theta=0.4, amp=0.8 if i in DIVERSE else 0.0)
                      for _ in range(3)]
            m = Module(name=f"slot{i}", cells=cells)
            if i in DIVERSE:
                for c, t in zip(m.cells, (1, 1, 1, 1, 1, 1)):
                    c.sigma = t
            modules[i] = m
            hashes[i] = f"{i:064x}"
        return modules, hashes

    def test_ladder_reduces_64_to_1_in_6_rounds(self):
        modules, hashes = self._leaves()
        params = Field(name="p", deadband=0.5)
        result = run_ladder(modules, hashes, params)
        self.assertEqual(len(result.rounds), 6)
        self.assertEqual([len(r.nodes) for r in result.rounds],
                         [32, 16, 8, 4, 2, 1])
        self.assertIsNotNone(result.root_node)
        self.assertEqual(len(result.round_roots), 6)

    def test_ladder_merkle_is_the_reduction_tree(self):
        """Recomputing pair hashes reproduces every node hash: same tree."""
        from gist_engine.crypto import merkle_node
        modules, hashes = self._leaves()
        params = Field(name="p", deadband=0.5)
        result = run_ladder(modules, hashes, params)
        r0 = result.rounds[0]
        bit = r0.bit
        for node in r0.nodes:
            # children names encode leaf addresses L0/xxxxxx
            a = int(node.children[0].split("/")[1], 2)
            b = int(node.children[1].split("/")[1], 2)
            self.assertEqual(b, a ^ (1 << bit))
            self.assertEqual(node.hash, merkle_node(hashes[a], hashes[b]))

    def test_ladder_deterministic(self):
        m1, h1 = self._leaves()
        m2, h2 = self._leaves()
        params = Field(name="p", deadband=0.5)
        r1 = run_ladder(m1, h1, params)
        r2 = run_ladder(m2, h2, params)
        self.assertEqual(r1.to_json(), r2.to_json())

    def test_fuse_pair_coherent_children(self):
        a = Module(name="a", cells=[Cell(theta=0.3, amp=1.0) for _ in range(6)])
        b = Module(name="b", cells=[Cell(theta=0.5, amp=1.0) for _ in range(6)])
        parent, gd = fuse_pair("p", a, b)
        self.assertEqual(len(parent.cells), 6)
        self.assertLessEqual(abs(gd), 0.2 + 1e-9)
        # parent belief = mean child write-cone kappa
        self.assertGreater(parent.belief, 0.8)


if __name__ == "__main__":
    unittest.main()
