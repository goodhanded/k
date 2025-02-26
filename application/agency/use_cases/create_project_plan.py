from application.agency.protocols.workflow import WorkflowProtocol

class CreateProjectPlanUseCase:
    """
    Use case for creating a project plan by invoking the project_plan workflow.
    It initializes a new project plan state with the provided prompt and executes the workflow.
    """
    def __init__(self, workflow: WorkflowProtocol):
        self.workflow = workflow

    def execute(self, prompt: str = None, stdin: bool = False, copy: bool = False) -> None:
        if stdin:
            prompt = stdin.read()
        if not prompt:
            print("No prompt provided. Aborting project plan creation.")
            return
        state = {"goal": prompt, "user_stories": None, "copy_prompt": copy}
        result = self.workflow.run(state)