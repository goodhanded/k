import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency.protocols.workflow import WorkflowProtocol
    from application.filesystem.protocols.clipboard import ClipboardProtocol


class CreatePullRequestUseCase:
    """
    Use case for creating a pull request by invoking the pull request workflow.
    It initializes a new state dictionary with the provided prompt as the goal,
    and includes decision variables for copying the prompt,
    then passes it to the workflow's run method.
    """

    def __init__(self, clipboard_service: 'ClipboardProtocol', workflow: 'WorkflowProtocol') -> None:
        self.clipboard_service = clipboard_service
        self.workflow = workflow

    def execute(self,
                prompt: str = None,
                include: str = None,
                stdin: bool = False,
                copy: bool = False,
                paste: bool = False,
                tree: bool = False,
                followup: bool = False) -> None:
        """
        Executes the pull request creation process.
        
        Parameters:
          - prompt: The prompt text to generate the pull request changes.
          - stdin: If True, read the prompt from standard input.
          - copy: If True, indicate that the generated PR prompt should be copied to the clipboard instead of invoking the LLM.
          - paste: If True, read the prompt from the clipboard.
          - tree: If True, print the directory tree to the console.
          - include: Override include patterns with a pipe-delimited list of glob patterns.
          - followup: If set, use followup mode to append to memory file and include its contents in the LLM prompt.
        """
        if stdin:
            prompt = sys.stdin.read()
        elif paste:
            prompt = self.clipboard_service.get()
        if not prompt:
            print("\nNo prompt provided. Aborting pull request creation.\n")
            return

        state = {
            "prompt": prompt,
            "copy_prompt": copy,
            "print_tree": tree,
            "include_override": include,
            "followup": followup
        }
        self.workflow.run(state)
