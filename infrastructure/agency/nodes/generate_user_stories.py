from pydantic import BaseModel, Field
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.language_models import BaseChatModel
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
    def __init__(self,chat_model: BaseChatModel, clipboard: ClipboardProtocol, prompt: TemplateProtocol, callback: callable = None) -> None:
        self.chat_model = chat_model
        self.clipboard = clipboard
        self.prompt = prompt
        self.callback = callback

    def __call__(self, state: dict) -> dict:
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        prompt = self.prompt.format(
            goal=state["goal"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )

        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt)
                print("Plan prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"user_stories": None, "progress": "Plan prompt copied to clipboard."}

        print("\nGenerating user stories. This may take a minute...\n")

        if self.callback:
            with self.callback() as cb:
                user_stories_plan = self.chat_model.with_structured_output(UserStoriesPlan).invoke([prompt])

            print(f"Input Tokens: {cb.prompt_tokens}")
            print(f"Output Tokens: {cb.completion_tokens}")
            print(f"Total: {cb.total_tokens}")
            print(f"Cost: {cb.total_cost}\n")
        else:
            user_stories_plan = self.chat_model.with_structured_output(UserStoriesPlan).invoke([prompt])

        print(f"Done. User Stories Summary: {user_stories_plan.summary}")

        return {"user_stories": user_stories_plan, "progress": "User stories generated."}
