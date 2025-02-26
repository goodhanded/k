import os
import unittest

from infrastructure.agency.nodes.implement_changeset import ImplementChangeset
from infrastructure.agency.nodes.generate_changeset import Changeset, FileChange


class TestImplementChangeset(unittest.TestCase):
    def test_implement_changeset(self):
        # Create a dummy changeset with additions, modifications, and removals.
        dummy_changeset = Changeset(
            summary="Dummy summary",
            additions=[FileChange(path="added.txt", content="Added content")],
            modifications=[FileChange(path="mod.txt", content="Modified content")],
            removals=[FileChange(path="remove.txt", content="")]
        )
        state = {
            "changeset": dummy_changeset,
            "project_path": os.getcwd()
        }
        node = ImplementChangeset()
        result = node(state)
        self.assertIn("Changeset implemented", result.get("progress", ""))


if __name__ == "__main__":
    unittest.main()