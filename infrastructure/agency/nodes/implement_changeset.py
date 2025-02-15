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

        if "project_path" not in state:
            raise ValueError("Project path not found in state.")

        changeset = state["changeset"]

        if not changeset:
            return {"progress": "No changeset to implement."}

        project_path = state["project_path"]

        for file_change in changeset.additions + changeset.modifications:
            abs_path = self._resolve_path(project_path, file_change.path)
            directory = os.path.dirname(abs_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(abs_path, 'w') as f:
                print(f"Writing to {abs_path}")
                f.write(file_change.content)
        
        for file_change in changeset.removals:
            abs_path = self._resolve_path(project_path, file_change.path)
            if os.path.exists(abs_path):
                print(f"Removing {abs_path}")
                os.remove(abs_path)
            else:
                print(f"File {abs_path} does not exist, cannot remove.")

        print(f"\nDone.\n")

        return {"progress": "Changeset implemented."}
    
    def _resolve_path(self, project_path: str, relative_path: str) -> str:
        full_path = os.path.abspath(os.path.join(project_path, relative_path))
        if not full_path.startswith(os.path.abspath(project_path)):
            raise ValueError(f"Unauthorized file path modification attempt: {relative_path}")
        return full_path
