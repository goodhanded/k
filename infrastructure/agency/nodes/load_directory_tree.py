import os

from typing import Optional

from application.agency import WorkflowNodeProtocol
from domain.filesystem import FileCollection

class LoadDirectoryTree(WorkflowNodeProtocol):
    """
    Load directory tree from the project path.
    """

    def __call__(self, state: dict) -> dict:
        """
        Load directory tree from the project path.

        Args:
            state (dict): State dictionary.
        """
        
        if "file_collection" not in state:
            raise ValueError("File collection not found in state.")

        file_collection = state["file_collection"]

        tree = file_collection.tree()

        print(tree)

        # Load directory tree
        return {"directory_tree": tree, "progress": "Directory tree loaded."}