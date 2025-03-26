from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.filesystem.protocols.clipboard import ClipboardProtocol
from application.templating.protocols.template import TemplateProtocol


class UserStory(BaseModel):
    title: str = Field(..., description="Title of the user story with format: As a <role>, I want <goal>, so that <benefit>")
    description: str = Field(..., description="Detailed description of the user story")
    acceptance_criteria: list[str] = Field(..., description="List of acceptance criteria in format 'GIVEN <context>, WHEN <action>, THEN <outcome>'")
    technical_considerations: list[str] = Field(..., description="List of technical considerations")
    steps_to_implement: list[str] = Field(..., description="Comprehensive and detailed list of steps to implement the user story. Include references to specific classes that need to be changed or created and what needs to be done in each step.")


class UserStoriesPlan(BaseModel):
    summary: str = Field(..., description="Summary of the project plan")
    user_stories: list[UserStory] = Field(..., description="List of user stories in order of priority")


class GenerateUserStories(WorkflowNodeProtocol):
    """
    Workflow node that generates user stories based on the provided goal.
    It uses an LLM to produce a structured list of user stories.
    """
    def __init__(self, clipboard: ClipboardProtocol, prompt: TemplateProtocol, model_id: str, model_config: dict = None) -> None:
        self.chat_model = init_chat_model(model_id, **(model_config or {}))
        self.clipboard = clipboard
        self.prompt = prompt

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Goal not found in state.")
        prompt_text = self.prompt.format(
            goal=state["prompt"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )

        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt_text)
                print("Plan prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"user_stories": None, "progress": "Plan prompt copied to clipboard."}

        print("\nGenerating user stories. This may take a minute...\n")

        user_stories_plan = self.chat_model.with_structured_output(UserStoriesPlan).invoke([prompt_text])

        print(f"Done. User Stories Summary: {user_stories_plan.summary}")

        return {"user_stories": user_stories_plan, "progress": "User stories generated."}
