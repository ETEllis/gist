"""Bridge codebook: bijection, addressing, and parity with the CDC repository."""

import unittest
from pathlib import Path

from gist_engine import bridge as B
from gist_engine.walks import from_word

CDC_REPO = Path(__file__).resolve().parents[2] / "bidi-coherence-delta-calculus"


class TestBridge(unittest.TestCase):
    def test_generated_codebook_is_bijective(self):
        rows = B.generate_codebook(6)
        self.assertEqual(len(rows), 64)
        self.assertTrue(B.verify_bijection(rows))

    def test_dyadic_triadic_roundtrip(self):
        for i in range(64):
            d = B.dyadic_of_index(i)
            t = B.dyadic_to_triadic(d)
            self.assertEqual(B.triadic_to_dyadic(t), d)
            self.assertEqual(B.index_of_dyadic(d), i)

    def test_known_cdc_rows(self):
        # bridge64.cdc: dyadic 101011 -> triadic 223 (index 43)
        self.assertEqual(B.dyadic_to_triadic("101011"), "223")
        # dyadic 101101 -> triadic 231 (index 45), the native surface witness
        self.assertEqual(B.dyadic_to_triadic("101101"), "231")
        self.assertEqual(B.index_of_dyadic("101101"), 45)
        # first and last rows
        self.assertEqual(B.dyadic_to_triadic("000000"), "000")
        self.assertEqual(B.dyadic_to_triadic("111111"), "333")

    def test_address_roundtrip(self):
        for i in range(64):
            q1, q2, q3 = B.address_of_index(i)
            self.assertEqual(B.index_of_address(q1, q2, q3), i)

    def test_trit_projection_matches_native_surface_witness(self):
        # native_surface.cdc: trace '+0-+0-' -> dyadic 101101, triadic 231
        row = B.project_trits(from_word("+0-+0-"))
        self.assertEqual(row.dyadic, "101101")
        self.assertEqual(row.triadic, "231")
        self.assertEqual(row.index, 45)

    def test_parity_with_cdc_bridge64_file(self):
        """Byte-level agreement with the actual CDC bridge64.cdc, if present."""
        path = CDC_REPO / "bridge64.cdc"
        if not path.exists():
            self.skipTest("CDC repository copy not present")
        self.assertTrue(B.parity_with_cdc(path, 6))

    def test_parity_with_cdc_bridge512_file(self):
        """The generated n=9 codebook (2^9 = 8^3) uses 3-bit groups, not pairs;
        only verify the loaded file is bijective and index-aligned by *its own*
        rule; the pairwise rule applies to even arities. Skip if absent."""
        path = CDC_REPO / "bridge512.cdc"
        if not path.exists():
            self.skipTest("CDC repository copy not present")
        rows = B.load_bridge_cdc(path)
        self.assertEqual(len(rows), 512)
        self.assertEqual(len({r.dyadic for r in rows}), 512)
        self.assertEqual(len({r.triadic for r in rows}), 512)


if __name__ == "__main__":
    unittest.main()
