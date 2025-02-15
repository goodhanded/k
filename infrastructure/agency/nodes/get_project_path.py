import os

from application.agency import WorkflowNodeProtocol

# Workflow Node: GetProjectPath
# This node retrieves the current project's absolute path (the working directory)
# and injects it into the workflow state for use by subsequent nodes.
class GetProjectPath(WorkflowNodeProtocol):
    """
    Workflow node that retrieves the current project path.

    The node does not depend on any input state and returns the current working directory.
    """

    def __call__(self, state: dict) -> dict:
        """
        Retrieves and returns the current project path.

        Returns:
            dict: Contains 'project_path' with the current working directory and a progress message.
        """
        # Retrieve current working directory as the project path.
        return {"project_path": os.getcwd(), "progress": "Project path loaded."}
