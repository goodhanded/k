import subprocess

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

# Workflow Node: RunTests
# This node executes the project's test suite using pytest,
# captures the output and exit status, and updates the workflow state with the test results.
class RunTests(WorkflowNodeProtocol):
    """
    Workflow node that runs the test suite and records the results.

    It executes 'pytest' as a subprocess, captures output and exit code,
    and returns whether tests passed along with the test output.
    """
    def __call__(self, state: dict) -> dict:
        """
        Executes the test suite:
          1. Runs 'pytest' and captures standard output.
          2. Determines if tests passed based on return code.
          3. Returns a state dictionary with test results and a progress message.
        """
        try:
            result = subprocess.run(["pytest"], capture_output=True, text=True)
            tests_passed = (result.returncode == 0)
        except Exception as e:
            return {"tests_passed": False, "test_output": str(e), "progress": "Tests failed to execute."}
        return {"tests_passed": tests_passed, "test_output": result.stdout, "progress": "Tests executed."}
