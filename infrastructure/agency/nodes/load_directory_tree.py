import os

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

# Workflow Node: LoadDirectoryTree
# This node creates a textual tree representation of the project's directory structure
# from the FileCollection.
class LoadDirectoryTree(WorkflowNodeProtocol):
    """
    Workflow node that generates a directory tree structure as a text representation.

    Utilizes the FileCollection to create a structured, human-readable overview
    of the project's directory and file organization.
    """

    def __call__(self, state: dict) -> dict:
        """
        Generate a directory tree string from the file collection.

        Requires 'file_collection' in the state.
        Returns:
            dict: Contains 'directory_tree' with the tree string and a progress message.
        """
        if "file_collection" not in state:
            raise ValueError("File collection not found in state.")

        file_collection = state["file_collection"]

        tree = file_collection.tree()

        print_tree = state.get("print_tree", False)
        if print_tree:
            print(f"\n{tree}")

        return {"directory_tree": tree, "progress": "Directory tree loaded."}
