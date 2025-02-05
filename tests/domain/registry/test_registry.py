import unittest

from domain.registry.entities.registry import Registry


class Dummy:
    def __init__(self, id, value):
        self.id = id
        self.value = value


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = Registry(services={})

    def test_register_and_get(self):
        dummy = Dummy("test1", "value1")
        self.registry.register(dummy)
        self.assertEqual(self.registry.get("test1").value, "value1")

    def test_iteration_and_length(self):
        dummy1 = Dummy("test1", "value1")
        dummy2 = Dummy("test2", "value2")
        self.registry.register(dummy1)
        self.registry.register(dummy2)
        items = list(self.registry)
        self.assertEqual(len(items), 2)


if __name__ == '__main__':
    unittest.main()
