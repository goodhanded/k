import subprocess

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

# Workflow Node: GitStatus
# This node executes the 'git status' command to retrieve the current source control status
# of the project, useful for integrating version control insights into workflows.
class GitStatus(WorkflowNodeProtocol):
    """
    Workflow node that retrieves Git status information from the project repository.
    """
    def __call__(self, state: dict) -> dict:
        """
        Run the 'git status' command and return its output.

        Returns:
            dict: Contains 'git_status' with the output of 'git status' and a progress message.
        """
        try:
            result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
            git_status = result.stdout.strip()
        except Exception as e:
            git_status = f"Error obtaining git status: {e}"
        return {"git_status": git_status, "progress": "Ran git status."}
