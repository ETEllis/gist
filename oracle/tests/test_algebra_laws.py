"""Law witnesses for the coherence algebra (mirrors laws.cdc invariants)."""

import cmath
import math
import unittest

from gist_engine import algebra as A


def close(a: complex, b: complex, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


class TestCarrier(unittest.TestCase):
    def test_interfere_monoid(self):
        """interfere-monoid: associative, commutative, unit VOID."""
        x, y, z = A.coh(1.0, 0.3), A.coh(0.5, 2.0), A.coh(2.0, -1.2)
        self.assertTrue(close(A.interfere(A.interfere(x, y), z),
                              A.interfere(x, A.interfere(y, z))))
        self.assertTrue(close(A.interfere(x, y), A.interfere(y, x)))
        self.assertTrue(close(A.interfere(x, A.VOID), x))

    def test_rotation_action(self):
        """rotation is a circle action by ⊞-automorphisms."""
        x, y = A.coh(1.0, 0.4), A.coh(0.7, -0.9)
        self.assertTrue(close(A.rotate(0.0, x), x))
        self.assertTrue(close(A.rotate(0.3, A.rotate(0.4, x)),
                              A.rotate(0.7, x)))
        # rotation-linear: distributes over interference
        self.assertTrue(close(A.rotate(1.1, A.interfere(x, y)),
                              A.interfere(A.rotate(1.1, x), A.rotate(1.1, y))))

    def test_amplitude_seminorm(self):
        x, y = A.coh(1.0, 0.4), A.coh(0.7, -0.9)
        self.assertEqual(A.amplitude(A.VOID), 0.0)
        self.assertAlmostEqual(A.amplitude(A.rotate(2.2, x)), A.amplitude(x), places=12)
        self.assertLessEqual(A.amplitude(A.interfere(x, y)),
                             A.amplitude(x) + A.amplitude(y) + 1e-12)

    def test_kappa_covariant_and_void(self):
        self.assertEqual(A.kappa(A.VOID), 0.0)
        x = A.coh(2.0, 0.25)
        self.assertAlmostEqual(A.kappa(x), math.cos(0.25), places=12)
        # κ is amplitude-independent (a cosine)
        self.assertAlmostEqual(A.kappa(A.coh(5.0, 0.25)), A.kappa(A.coh(0.1, 0.25)), places=12)

    def test_balanced_ternary_derivation(self):
        """balanced-ternary-carrier: trits derive from κ with deadband 1/2."""
        self.assertEqual(A.trit(A.coh(1.0, 0.0)), 1)          # κ = 1
        self.assertEqual(A.trit(A.coh(1.0, math.pi)), -1)     # κ = -1
        self.assertEqual(A.trit(A.coh(1.0, math.pi / 2)), 0)  # κ = 0 crossing
        self.assertEqual(A.trit(A.VOID), 0)
        # balance: -1 + 0 + 1 = 0 around equilibrium
        self.assertEqual(sum((-1, 0, 1)), 0)

    def test_openness_maximal_at_crossing(self):
        self.assertAlmostEqual(A.openness(A.coh(1.0, math.pi / 2)), 1.0, places=12)
        self.assertAlmostEqual(A.openness(A.coh(1.0, 0.0)), 0.0, places=12)


class TestGateGroup(unittest.TestCase):
    def test_gate_abelian_group(self):
        """gate-abelian: associative, commutative, identity, inverse (≅ Tⁿ)."""
        a = (0.5, -1.2, 3.0)
        b = (1.0, 2.0, -0.7)
        c = (-2.5, 0.1, 0.9)
        ab_c = A.gate(A.gate(a, b), c)
        a_bc = A.gate(a, A.gate(b, c))
        for x, y in zip(ab_c, a_bc):
            self.assertAlmostEqual(x, y, places=12)
        for x, y in zip(A.gate(a, b), A.gate(b, a)):
            self.assertAlmostEqual(x, y, places=12)
        for x, y in zip(A.gate(a, A.gate_identity(3)), a):
            self.assertAlmostEqual(x, y, places=12)
        for x in A.gate(a, A.gate_inverse(a)):
            self.assertAlmostEqual(math.sin(x), 0.0, places=12)  # 0 on the torus


class TestCorefold(unittest.TestCase):
    def test_corefold_morphism(self):
        """corefold-morphism: ⊞-linear and ⟳-equivariant, strictly abstracting."""
        t1 = (A.coh(1, 0.2), A.coh(1, 1.0), A.coh(1, -0.5))
        t2 = (A.coh(0.5, 2.0), A.coh(2.0, 0.0), A.coh(1.0, 3.0))
        # linear: ∂(x ⊞ y) = ∂x ⊞ ∂y   (componentwise)
        summed = tuple(a + b for a, b in zip(t1, t2))
        f_sum = A.corefold_3_to_2(summed)
        f_parts = tuple(a + b for a, b in zip(A.corefold_3_to_2(t1), A.corefold_3_to_2(t2)))
        for x, y in zip(f_sum, f_parts):
            self.assertTrue(close(x, y))
        # equivariant: ∂(⟳x) = ⟳(∂x)
        rot = tuple(A.rotate(0.8, v) for v in t1)
        f_rot = A.corefold_3_to_2(rot)
        rot_f = tuple(A.rotate(0.8, v) for v in A.corefold_3_to_2(t1))
        for x, y in zip(f_rot, rot_f):
            self.assertTrue(close(x, y))
        # strictly abstracting: not injective (distinct triads can fold equal)
        u = (A.coh(1, 0.0), A.VOID, A.coh(1, 0.0))
        w = (A.VOID, A.coh(1, 0.0), A.VOID)
        fu, fw = A.corefold_3_to_2(u), A.corefold_3_to_2(w)
        self.assertTrue(close(fu[0], fw[0]) and close(fu[1], fw[1]))
        self.assertNotEqual(u, w)

    def test_corefold_pyramid_3_2_1(self):
        """The 3→2→1 distillation pyramid is well-defined and linear."""
        t = (A.coh(1, 0.1), A.coh(1, 0.2), A.coh(1, 0.3))
        d = A.corefold_3_to_2(t)
        s = A.corefold_2_to_1(d)
        expected = (t[0] + 2 * t[1] + t[2]) / 4.0
        self.assertTrue(close(s, expected))

    def test_corefold_middle_n6(self):
        cells = [A.coh(1, 0.1 * i) for i in range(6)]
        mid = A.corefold_middle(cells)
        self.assertTrue(close(mid, (cells[2] + cells[3]) / 2.0))


class TestPhaseOrder(unittest.TestCase):
    def test_bounds_and_alignment(self):
        aligned = [A.coh(1.0, 0.5)] * 4
        self.assertAlmostEqual(A.phase_order(aligned), 1.0, places=12)
        opposed = [A.coh(1.0, 0.0), A.coh(1.0, math.pi)]
        self.assertAlmostEqual(A.phase_order(opposed), 0.0, places=12)
        self.assertEqual(A.phase_order([]), 0.0)

    def test_coherence_delta(self):
        a, b = A.coh(1.0, 1.0), A.coh(2.0, 0.25)
        self.assertAlmostEqual(A.coherence_delta(a, b), 0.75, places=12)


if __name__ == "__main__":
    unittest.main()
