import subprocess

from application.agency import WorkflowNodeProtocol


class GitStatus(WorkflowNodeProtocol):
    """
    Loads source control information for the project using git status.
    """
    def __call__(self, state: dict) -> dict:
        try:
            result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
            git_status = result.stdout.strip()
        except Exception as e:
            git_status = f"Error obtaining git status: {e}"
        return {"git_status": git_status, "progress": "Ran git status."}
