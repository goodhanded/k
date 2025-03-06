import os
from typing import Any
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.util.project_root import find_project_root


# Workflow Node: GetProjectPath
# This node retrieves the current project's absolute path by using the shared utility function.
class GetProjectPath(WorkflowNodeProtocol):
    """
    Workflow node that retrieves the current project path.

    It uses the shared utility function 'find_project_root' to determine the project root.
    """

    def __call__(self, state: dict) -> dict:
        project_path = find_project_root()
        if project_path is None:
            print("Project directory not found. Call k init to initialize a project.")
            exit(1)
        return {"project_path": project_path, "progress": "Project path loaded."}
