"""torchcdc battery: autograd, native labeling, training, export parity.

Run:  python3 test_torchcdc.py
"""

import json
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402
import hybrid  # noqa: E402
import tensorcdc as tc  # noqa: E402
import train  # noqa: E402


class TestAutograd(unittest.TestCase):
    def test_gradcheck_through_composed_graph(self):
        rng = np.random.default_rng(0)
        w = tc.param(rng.uniform(-1, 1, 5))
        x = tc.param(rng.uniform(-1, 1, 5))

        def value():
            return float(np.sum(np.sin(w.v) * np.cos(x.v) + w.v * x.v))

        out = tc.total(tc.add(tc.mul(tc.sin(w), tc.cos(x)), tc.mul(w, x)))
        out.backward()
        eps = 1e-6
        for t in (w, x):
            for i in range(5):
                orig = t.v[i]
                t.v[i] = orig + eps
                up = value()
                t.v[i] = orig - eps
                dn = value()
                t.v[i] = orig
                self.assertAlmostEqual(t.g[i], (up - dn) / (2 * eps),
                                       places=5)

    def test_ste_trit(self):
        k = tc.param(np.array([0.9, 0.1, -0.8]))
        t = tc.ste_trit(k)
        self.assertEqual(t.v.tolist(), [1.0, 0.0, -1.0])
        tc.total(t).backward()
        self.assertEqual(k.g.tolist(), [1.0, 1.0, 1.0])

    def test_scatter_gather_roundtrip(self):
        a = tc.param(np.array([[1.0, 2.0, 3.0]]))
        s = tc.scatter_sum(a, np.array([0, 0, 1]), 2)
        self.assertEqual(s.v.tolist(), [[3.0, 3.0]])
        tc.total(s).backward()
        self.assertEqual(a.g.tolist(), [[1.0, 1.0, 1.0]])


class TestNativeLabeling(unittest.TestCase):
    def test_deterministic_and_balanced(self):
        t1 = data.build_dataset(40, 8, seed=3)
        t2 = data.build_dataset(40, 8, seed=3)
        self.assertTrue((t1[3] == t2[3]).all())
        self.assertTrue((t1[4] == t2[4]).all())
        labels = set(t1[3][t1[2]].tolist())
        self.assertEqual(labels, {-1, 0, 1})

    def test_labels_come_from_the_runtime(self):
        """A hand-built decisive cone must label +1 factually and -1 mirrored."""
        strong = [(2.2, 0.45), (0.0, np.pi / 2), (0.5, 2.4)]
        labels, fw, mw = data.native_slot_labels([strong])
        self.assertEqual(labels[0], 1)
        against = [(2.2, np.pi - 0.45), (0.0, np.pi / 2), (0.5, np.pi - 2.4)]
        labels2, _, _ = data.native_slot_labels([against])
        self.assertEqual(labels2[0], -1)


class TestTrainingAndParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train_set = data.build_dataset(160, 8, seed=31)
        cls.val_set = data.build_dataset(60, 8, seed=32)
        cls.test_set = data.build_dataset(60, 8, seed=33)

    def test_calculus_init_beats_random_untrained(self):
        calc = hybrid.GistHybrid(bits=3).init_calculus()
        rand_scores = [
            train.evaluate(hybrid.GistHybrid(bits=3).init_random(s),
                           *self.test_set)["score"]
            for s in range(1, 5)
        ]
        calc_score = train.evaluate(calc, *self.test_set)["score"]
        self.assertGreater(calc_score, float(np.mean(rand_scores)))

    def test_short_training_improves(self):
        m = hybrid.GistHybrid(bits=3).init_calculus()
        before = train.evaluate(m, *self.test_set)["score"]
        train.fit(m, self.train_set, self.val_set, max_epochs=6, patience=6)
        after = train.evaluate(m, *self.test_set)["score"]
        self.assertGreater(after, before)

    def test_save_load_roundtrip(self):
        m = hybrid.GistHybrid(bits=3).init_calculus()
        train.fit(m, self.train_set, self.val_set, max_epochs=2, patience=2)
        d = m.export_weights()
        m2 = hybrid.GistHybrid.load(json.loads(json.dumps(d)))
        th, am, occ, sy, gy = self.test_set
        p1 = m.predict(th[:8], am[:8])
        p2 = m2.predict(th[:8], am[:8])
        self.assertTrue((p1[0] == p2[0]).all())
        self.assertTrue((p1[1] == p2[1]).all())

    def test_deploy_native_parity(self):
        """Trained-or-not, the deploy model and the exported .cdc agree."""
        m = hybrid.GistHybrid(bits=0, steps=4, lattice=False,
                              deploy=True).init_calculus()
        path = os.path.join(train.BUILD, "parity_check.cdc")
        os.makedirs(train.BUILD, exist_ok=True)
        train.export_deploy_cdc(m, path)
        matches, total, _ = train.native_parity(m, path)
        self.assertEqual(matches, total)


class TestResultsArtifact(unittest.TestCase):
    def test_results_exist_and_hold_the_bars(self):
        """The published claims are backed by the committed results.json."""
        path = os.path.join(train.BUILD, "results.json")
        if not os.path.exists(path):
            self.skipTest("run train.py first")
        r = json.load(open(path))
        self.assertGreaterEqual(r["primary"]["trained_test"]["slot_acc"],
                                0.95)
        self.assertGreaterEqual(r["primary"]["trained_test"]["global_acc"],
                                0.80)
        self.assertGreater(
            r["primary"]["trained_test"]["slot_acc"],
            r["baselines"]["majority_slot_acc"] + 0.2)
        m, t = r["deployment"]["native_parity"].split("/")
        self.assertEqual(m, t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
