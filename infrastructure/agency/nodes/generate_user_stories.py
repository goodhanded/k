from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol
from application.filesystem import ClipboardProtocol
from application.templating import TemplateProtocol


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
    def __init__(self, clipboard: ClipboardProtocol, prompt_adapter: TemplateProtocol, model: str):
        self.clipboard = clipboard
        self.prompt_adapter = prompt_adapter
        self.model = model

    def __call__(self, state: dict) -> dict:
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        prompt = self.prompt_adapter.format(
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

        llm = ChatOpenAI(model=self.model, reasoning_effort="high")

        print("\nGenerating user stories. This may take a minute...\n")

        with get_openai_callback() as cb:
            user_stories_plan = llm.with_structured_output(UserStoriesPlan).invoke([prompt])
        print(f"Done. User Stories Summary: {user_stories_plan.summary}")
        state["user_stories"] = user_stories_plan
        return {"user_stories": user_stories_plan, "progress": "User stories generated."}
