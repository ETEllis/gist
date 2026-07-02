"""GistSSM: the trainable GIST-native architecture actually learns.

The claims under test, per the signed directive:
  - the dataset is oracle-labeled (the engine labels its own supervision);
  - initializing at the calculus transfers (beats random init untrained);
  - training on cdcgrad genuinely learns (loss falls, held-out accuracy
    lands well above chance and above the untrained calculus init);
  - the whole thing is deterministic and exportable.
"""

import unittest

from gist_engine import cdcgrad as G
from gist_engine.gistnet import GistSSM, make_dataset

TRAIN_N = 220
TEST_N = 80
EPOCHS = 8
LR = 0.01


class TestDataset(unittest.TestCase):
    def test_deterministic_and_labeled_by_oracle(self):
        d1 = make_dataset(40, seed=3)
        d2 = make_dataset(40, seed=3)
        self.assertEqual([s.label for s in d1], [s.label for s in d2])
        self.assertEqual([s.theta for s in d1], [s.theta for s in d2])
        labels = {s.label for s in make_dataset(200, seed=1)}
        self.assertEqual(labels, {-1, 0, 1})  # all three classes appear


class TestAutograd(unittest.TestCase):
    def test_gradcheck_core_ops(self):
        """Finite-difference check through the composed CDC op graph."""
        w = G.tensor([0.4, -0.3], requires_grad=True)
        x = G.tensor([0.7, 0.2], requires_grad=True)
        out = G.total(G.mul(G.sin(w), G.cos(x)))
        out.backward()
        eps = 1e-6
        for t in (w, x):
            for i in range(len(t)):
                orig = t.data[i]
                t.data[i] = orig + eps
                up = _value(w, x)
                t.data[i] = orig - eps
                dn = _value(w, x)
                t.data[i] = orig
                self.assertAlmostEqual(t.grad[i], (up - dn) / (2 * eps),
                                       places=5)

    def test_ste_trit_forward_hard_backward_open(self):
        k = G.tensor([0.9, 0.1, -0.8], requires_grad=True)
        t = G.ste_trit(k)
        self.assertEqual(t.data, [1.0, 0.0, -1.0])
        G.total(t).backward()
        self.assertEqual(k.grad, [1.0, 1.0, 1.0])  # straight through


def _value(w, x):
    import math
    return sum(math.sin(a) * math.cos(b) for a, b in zip(w.data, x.data))


class TestTraining(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train = make_dataset(TRAIN_N, seed=11)
        cls.test = make_dataset(TEST_N, seed=99)

    def test_calculus_init_transfers(self):
        """Untrained: the calculus initialization dominates random inits."""
        calc = GistSSM().init_calculus()
        acc_calc = calc.accuracy(self.test)
        rand_accs = [
            GistSSM().init_random(seed=s).accuracy(self.test)
            for s in range(1, 6)
        ]
        self.assertGreater(acc_calc, sum(rand_accs) / len(rand_accs) + 0.2)
        self.assertGreater(acc_calc, 0.7)

    def test_training_learns_to_anticipate_the_gate(self):
        from collections import Counter

        model = GistSSM().init_calculus()
        acc_before = model.accuracy(self.test)
        history = model.fit(self.train, epochs=EPOCHS, lr=LR)
        acc_after = model.accuracy(self.test)
        majority_label = Counter(
            s.label for s in self.train).most_common(1)[0][0]
        majority = sum(
            1 for s in self.test if s.label == majority_label
        ) / len(self.test)
        self.assertLess(history[-1], history[0] * 0.75)  # loss fell >= 25%
        self.assertGreater(acc_after, acc_before)        # training helps
        self.assertGreaterEqual(acc_after, 0.85)         # strong final
        self.assertGreater(acc_after, majority + 0.1)    # far above baseline
        # tiny model: the essence is compressed, not sprawling
        self.assertLess(model.n_params(), 100)

    def test_deterministic_training(self):
        def run():
            m = GistSSM().init_calculus()
            m.fit(self.train[:60], epochs=2, lr=LR)
            return m.export_weights()
        self.assertEqual(run(), run())

    def test_export_shape(self):
        m = GistSSM().init_calculus()
        w = m.export_weights()
        self.assertEqual(len(w["w"]), 6)
        self.assertEqual(len(w["w_out"]), 54)
        self.assertEqual(w["architecture"], "GistSSM/slot-cell")


if __name__ == "__main__":
    unittest.main()
