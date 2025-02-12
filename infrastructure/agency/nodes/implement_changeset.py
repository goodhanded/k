import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from application.agency import WorkflowNodeProtocol
from adapters.prompts import PullRequestPrompt

class ImplementChangeset(WorkflowNodeProtocol):
    """
    Implement a changeset.
    """

    def __call__(self, state: dict) -> dict:
        """
        Implement a changeset.

        Args:
            state (dict): State dictionary.
        """
        
        if "changeset" not in state:
            raise ValueError("Changeset not found in state.")

        changeset = state["changeset"]

        for file_change in changeset.additions + changeset.modifications:
            abs_path = self._resolve_path(file_change.path)
            directory = os.path.dirname(abs_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(abs_path, 'w') as f:
                print(f"Writing to {abs_path}")
                f.write(file_change.content)
        
        for file_change in changeset.removals:
            abs_path = self._resolve_path(file_change.path)
            if os.path.exists(abs_path):
                print(f"Removing {abs_path}")
                os.remove(abs_path)
            else:
                print(f"File {abs_path} does not exist, cannot remove.")

        print(f"\nDone.\n")

        return {"progress": "Changeset implemented."}
    