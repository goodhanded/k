import os

from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from domain.filesystem.entities.file_collection import FileCollection

# Workflow Node: LoadSourceCode
# This node converts the previously loaded FileCollection into a markdown representation,
# aggregating the source code of the files in the project.
class LoadSourceCode(WorkflowNodeProtocol):
    """
    Workflow node that extracts source code from the file collection.

    Converts the FileCollection into a markdown formatted string, which can be
    used for review or comparative analysis.
    """

    def __call__(self, state: dict) -> dict:
        """
        Generate a markdown representation of the project's source code.

        Requires 'file_collection' in the state.
        Returns:
            dict: Contains 'source_code' as a markdown string and a progress message.
        """
        if "file_collection" not in state:
            raise ValueError("File collection not found in state.")

        file_collection = state["file_collection"]
        project_path = state["project_path"]

        return {"source_code": file_collection.to_markdown(base_path=project_path), "progress": "Source code loaded."}
