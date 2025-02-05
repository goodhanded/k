import os
import unittest

from infrastructure.config.services.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        # Set environment variable temporarily
        os.environ["TEST_VAR"] = "test_value"

    def tearDown(self):
        if "TEST_VAR" in os.environ:
            del os.environ["TEST_VAR"]

    def test_get_existing(self):
        config = Config()
        self.assertEqual(config.get("TEST_VAR"), "test_value")

    def test_get_non_existing(self):
        config = Config()
        self.assertIsNone(config.get("NON_EXISTENT_VAR"))

    def test_require_existing(self):
        config = Config()
        self.assertEqual(config.require("TEST_VAR"), "test_value")

    def test_require_missing(self):
        config = Config()
        with self.assertRaises(ValueError):
            config.require("MISSING_VAR")


if __name__ == '__main__':
    unittest.main()
