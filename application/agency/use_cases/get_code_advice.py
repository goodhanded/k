from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import WorkflowProtocol


class GetCodeAdviceUseCase:
    """
    Use case for generating advice on an existing code base.
    It initializes a new state dictionary with the provided prompt as the goal,
    and passes it to the workflow's run method. Additional flags support reading the prompt from stdin,
    copying the generated pull request prompt to the clipboard instead of invoking the LLM, and token count confirmation.
    """

    def __init__(self, workflow: 'WorkflowProtocol') -> None:
        self.workflow = workflow

    def execute(self, prompt: str = None) -> None:
        """
        Executes the advice generation.

        Parameters:
          - prompt: The prompt text containing a specific question.
        """


        # Proceed with executing the pull request workflow
        state = {"prompt": prompt}
        self.workflow.run(state)
