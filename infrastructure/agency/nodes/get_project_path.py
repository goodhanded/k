import os

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

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
        # Save the original working directory
        project_path = os.getcwd()

        # Look for .k directory by traversing up the directory tree
        while not os.path.exists(os.path.join(project_path, ".k")):
            parent_dir = os.path.dirname(project_path)
            if parent_dir == project_path:  # Reached root directory
                print("Project directory not found. Call k init to initialize a project.")
                exit(1)
            project_path = parent_dir

        return {"project_path": project_path, "progress": "Project path loaded."}
