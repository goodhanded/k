from typing import TypedDict

class RunTestsWorkflowState(TypedDict):
    """
    Workflow state for the run tests workflow.

    Fields:
      - tests_passed: Boolean flag indicating whether tests passed.
      - test_output: The output of the test suite.
      - progress: The progress message
    """

    tests_passed: bool
    test_output: str
    progress: str
