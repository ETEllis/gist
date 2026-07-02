"""The native contract: every gist.cdc witness runs green as a live check."""

import unittest

from gist_engine.contract import REGISTRY, contract_path, verify_contract
from gist_engine import cdcread


class TestContract(unittest.TestCase):
    def test_contract_file_parses(self):
        program = cdcread.parse_file(contract_path())
        self.assertTrue(program.all("kernel"))
        self.assertGreaterEqual(len(program.all("witness")), 28)
        self.assertGreaterEqual(len(program.all("invariant")), 17)

    def test_every_witness_names_a_live_check(self):
        program = cdcread.parse_file(contract_path())
        for w in program.all("witness"):
            self.assertIn(w.get("check"), REGISTRY,
                          f"witness {w.key} has no live check")

    def test_full_contract_verifies(self):
        report = verify_contract()
        failing = [c for c in report["checks"] if not c["passed"]]
        self.assertTrue(report["verified"], failing)
        self.assertEqual(report["passed"], report["total"])
        self.assertTrue(report["expectations_ok"])


if __name__ == "__main__":
    unittest.main()
