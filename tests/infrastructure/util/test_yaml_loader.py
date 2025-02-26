import os
import tempfile
import unittest

from infrastructure.util.yaml_loader import YamlLoader


class TestYamlLoader(unittest.TestCase):
    def setUp(self):
        self.temp_yaml = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".yaml")
        self.temp_yaml.write("""
services:
  test_service:
    class: test.module.ClassName
    arguments: [ "arg1", "arg2" ]
""")
        self.temp_yaml.close()
        self.loader = YamlLoader()

    def tearDown(self):
        os.unlink(self.temp_yaml.name)

    def test_load_full_yaml(self):
        content = self.loader.load_yaml(self.temp_yaml.name)
        self.assertIn("services", content)
        self.assertIn("test_service", content["services"])

    def test_load_subpath(self):
        service = self.loader.load_yaml(self.temp_yaml.name, subpath=["services", "test_service"])
        self.assertIsInstance(service, dict)
        self.assertEqual(service.get("class"), "test.module.ClassName")


if __name__ == '__main__':
    unittest.main()
