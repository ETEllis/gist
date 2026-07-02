"""The finite n=6 normal-form spectrum: 729 / 267 / 51 / 20 / 5.

These are the exact counts declared by the CDC native proof job
(`proof trit-walk-n6` in native_reducer.cdc) and the calculus's metatheorem
T5 census (directed-animal / Motzkin / central-binomial / Catalan).
"""

import unittest

from gist_engine import walks as W


class TestSpectrum(unittest.TestCase):
    def test_census_n6_matches_cdc_proof(self):
        self.assertEqual(W.census(6), W.CDC_N6_SPECTRUM)
        self.assertEqual(W.census(6), {
            "total": 729,
            "admissible": 267,
            "localized": 51,
            "saturated": 20,
            "catalan": 5,
        })

    def test_census_small_arity_sanity(self):
        # n=2: 9 words; admissible: (00,0+,+0,++,+-)=5; localized: 00,+- =2;
        # saturated: +-,-+ = 2; catalan: +- = 1
        self.assertEqual(W.census(2), {
            "total": 9, "admissible": 5, "localized": 2,
            "saturated": 2, "catalan": 1,
        })


class TestPredicates(unittest.TestCase):
    def test_native_reducer_witness_words(self):
        # accepted case from native_reducer.cdc: '0+-' admissible
        self.assertTrue(W.is_admissible(W.from_word("0+-")))
        # hold case: '-+0' violates at the first cell
        self.assertFalse(W.is_admissible(W.from_word("-+0")))
        self.assertEqual(W.first_violation(W.from_word("-+0")), 0)

    def test_walk_and_words(self):
        self.assertEqual(W.walk((1, -1, 0, 1)), (1, 0, 0, 1))
        self.assertEqual(W.to_word((0, 1, -1)), "0+-")
        self.assertEqual(W.from_word("0+-"), (0, 1, -1))

    def test_classification_hierarchy(self):
        self.assertEqual(W.classify(W.from_word("+-+-+-")), "catalan")
        self.assertEqual(W.classify(W.from_word("+0-+0-")), "localized")
        self.assertEqual(W.classify(W.from_word("++0000")), "admissible")
        self.assertEqual(W.classify(W.from_word("-+++++")), "inadmissible")
        # saturated but inadmissible stays inadmissible (barrier outranks)
        self.assertTrue(W.is_saturated(W.from_word("-+-+-+")))
        self.assertEqual(W.classify(W.from_word("-+-+-+")), "inadmissible")

    def test_occupancy_projection(self):
        # native_surface.cdc witness: trits +0-+0- -> dyadic 101101
        self.assertEqual(W.occupancy_bits(W.from_word("+0-+0-")), "101101")


if __name__ == "__main__":
    unittest.main()
