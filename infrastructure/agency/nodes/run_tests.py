import subprocess

from application.agency import WorkflowNodeProtocol


class RunTests(WorkflowNodeProtocol):
    """
    Executes the test suite using pytest and sets the test outcome in the state.
    """
    def __call__(self, state: dict) -> dict:
        try:
            result = subprocess.run(["pytest"], capture_output=True, text=True)
            tests_passed = (result.returncode == 0)
        except Exception as e:
            tests_passed = False
        return {"tests_passed": tests_passed, "test_output": result.stdout, "progress": "Tests executed."}
