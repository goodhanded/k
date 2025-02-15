import unittest
from unittest.mock import patch, MagicMock
from infrastructure.agency.nodes.run_tests import RunTests


class TestRunTests(unittest.TestCase):
    @patch("infrastructure.agency.nodes.run_tests.subprocess.run")
    def test_run_tests_passed(self, mock_run):
        dummy_result = MagicMock()
        dummy_result.returncode = 0
        dummy_result.stdout = "All tests passed."
        mock_run.return_value = dummy_result

        node = RunTests()
        state = {}
        result = node(state)
        self.assertIn("tests_passed", result)
        self.assertTrue(result["tests_passed"])
        self.assertEqual(result["test_output"], "All tests passed.")
        self.assertEqual(result["progress"], "Tests executed.")

    @patch("infrastructure.agency.nodes.run_tests.subprocess.run")
    def test_run_tests_failed(self, mock_run):
        dummy_result = MagicMock()
        dummy_result.returncode = 1
        dummy_result.stdout = "Some tests failed."
        mock_run.return_value = dummy_result

        node = RunTests()
        state = {}
        result = node(state)
        self.assertFalse(result["tests_passed"])
        self.assertEqual(result["test_output"], "Some tests failed.")
        self.assertEqual(result["progress"], "Tests executed.")


if __name__ == '__main__':
    unittest.main()
