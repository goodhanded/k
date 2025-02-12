import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import WorkflowProtocol


class RunTestsUseCase:
    """
    Use case for creating a pull request by invoking the pull request workflow.
    It initializes a new state dictionary with the provided prompt as the goal,
    and passes it to the workflow's run method. Additional flags support reading the prompt from stdin,
    copying the generated pull request prompt to the clipboard instead of invoking the LLM, and token count confirmation.
    """

    def __init__(self, workflow: 'WorkflowProtocol') -> None:
        self.workflow = workflow

    def execute(self) -> None:
        """
        Runs the tests.
        """
        # Proceed with executing the pull request workflow
        state = { "tests_passed": False, "test_output": "", "progress": "Tests not executed." }
        result = self.workflow.run(state)
        print(result["test_output"])