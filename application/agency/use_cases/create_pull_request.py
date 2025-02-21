import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import WorkflowProtocol
    from application.filesystem import ClipboardProtocol


class CreatePullRequestUseCase:
    """
    Use case for creating a pull request by invoking the pull request workflow.
    It initializes a new state dictionary with the provided prompt as the goal,
    and includes decision variables for confirmation and copying the prompt,
    then passes it to the workflow's run method.
    """

    def __init__(self, clipboard_service: 'ClipboardProtocol', workflow: 'WorkflowProtocol') -> None:
        self.clipboard_service = clipboard_service
        self.workflow = workflow

    def execute(self,
                prompt: str = None,
                stdin: bool = False,
                paste: bool = False,
                copy: bool = False,
                confirm: bool = False,
                tree: bool = False) -> None:
        """
        Executes the pull request creation process.
        
        Parameters:
          - prompt: The prompt text to generate the pull request changes.
          - stdin: If True, read the prompt from standard input.
          - paste: If True, read the prompt from the clipboard.
          - copy: If True, indicate that the generated PR prompt should be copied to the clipboard instead of invoking the LLM.
          - confirm: If True, require user confirmation after token counting before proceeding with the LLM invocation.
        """
        if stdin:
            prompt = sys.stdin.read()
        elif paste:
            prompt = self.clipboard_service.get()
        if not prompt:
            print("No prompt provided. Aborting pull request creation.")
            return

        state = {
            "goal": prompt,
            "confirmation_required": confirm,
            "copy_prompt": copy,
            "print_tree": tree
        }
        self.workflow.run(state)