import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from application.agency import WorkflowNodeProtocol
from adapters.prompts import PullRequestPrompt

# Workflow Node: ImplementChangeset
# This node applies the changeset to the project files by processing file additions, modifications, and removals.
# It ensures paths are resolved safely, creates directories when necessary, writes new file contents, and deletes removed files.
class ImplementChangeset(WorkflowNodeProtocol):
    """
    Workflow node that implements the generated changeset by modifying the project's files.

    It reads the 'changeset' and 'project_path' from the state,
    then iterates over additions, modifications, and removals to update the filesystem accordingly.
    """

    def __call__(self, state: dict) -> dict:
        """
        Implements the changeset by writing new file contents and removing files as specified.

        Steps:
          1. Validate that 'changeset' and 'project_path' are present in the state.
          2. For each file in additions and modifications:
             - Resolve the absolute path.
             - Create necessary directories if they do not exist.
             - Write the complete new file content.
          3. For each file in removals:
             - Resolve the absolute path and delete the file if it exists.
          4. Print completion message and return progress state.
        """
        if "changeset" not in state:
            raise ValueError("Changeset not found in state.")

        if "project_path" not in state:
            raise ValueError("Project path not found in state.")

        changeset = state["changeset"]

        if not changeset:
            return {"progress": "No changeset to implement."}

        project_path = state["project_path"]

        # Process file additions and modifications.
        for file_change in changeset.additions + changeset.modifications:
            abs_path = self._resolve_path(project_path, file_change.path)
            directory = os.path.dirname(abs_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(abs_path, 'w') as f:
                print(f"Writing to {abs_path}")
                f.write(file_change.content)
        
        # Process file removals.
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
        """
        Resolves the absolute path of a file based on a relative path and the project base path.

        Ensures that the resolved path is within the project directory to prevent unauthorized modifications.
        """
        full_path = os.path.abspath(os.path.join(project_path, relative_path))
        if not full_path.startswith(os.path.abspath(project_path)):
            raise ValueError(f"Unauthorized file path modification attempt: {relative_path}")
        return full_path
