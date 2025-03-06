import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency.protocols.workflow import WorkflowProtocol
    from application.filesystem.protocols.clipboard import ClipboardProtocol

class GetCodeAdviceUseCase:
    """
    Use case for generating advice on an existing code base.
    It initializes a new state dictionary with the provided prompt as the goal,
    and passes it to the workflow's run method. Additional flags support reading the prompt from stdin and
    copying the generated prompt to the clipboard instead of invoking the LLM.
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
        Executes the advice generation.

        Parameters:
          - prompt: The prompt text containing a specific question.
          - stdin: If True, read the prompt from standard input instead of command-line argument.
          - tree: If True, print the directory tree to the console.
          - copy: If True, copy the generated prompt to the clipboard instead of invoking the LLM.
          - followup: If set, append this invocation's prompt and response to a memory file and include its contents in the LLM prompt for incremental updates.
        """
        if stdin:
            prompt = sys.stdin.read()
        elif paste:
            prompt = self.clipboard_service.get()
        if not prompt:
            print("No prompt provided. Aborting advice generation.")
            return

        state = {
            "prompt": prompt,
            "copy_prompt": copy,
            "print_tree": tree,
            "include_override": include,
            "followup": followup
        }
        self.workflow.run(state)
