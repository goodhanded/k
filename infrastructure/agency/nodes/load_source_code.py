import os

from typing import Optional

from application.agency import WorkflowNodeProtocol
from domain.filesystem import FileCollection

class LoadSourceCode(WorkflowNodeProtocol):
    """
    Load source code from the file collection.
    """

    def __call__(self, state: dict) -> dict:
        """
        Load source code from the file collection.

        Args:
            state (dict): State dictionary.
        """
        
        if "file_collection" not in state:
            raise ValueError("File collection not found in state.")

        file_collection = state["file_collection"]

        return {"source_code": file_collection.to_markdown(), "progress": "Source code loaded."}
    