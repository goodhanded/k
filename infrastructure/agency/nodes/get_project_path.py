import os

from application.agency import WorkflowNodeProtocol

class GetProjectPath(WorkflowNodeProtocol):
    """
    Get the current project path.
    """

    def __call__(self, state: dict) -> dict:
        """
        Get the current project path.

        Args:
            state (dict): State dictionary.
        """

        # Load directory tree
        return {"project_path": os.getcwd(), "progress": "Project path loaded."}