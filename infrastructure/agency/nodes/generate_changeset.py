import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol
from adapters.prompts import PullRequestPrompt


class FileChange(BaseModel):
    path: str = Field(..., description="Relative path to the file within the project.")
    content: Optional[str] = Field(None, description="Content of the file. Include the ENTIRE file content, not just the changes. Don't forget imports, etc.")

class Changeset(BaseModel):
    summary: str = Field(..., description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: list[FileChange] = Field(..., description="List of files added.")
    removals: list[FileChange] = Field(..., description="List of files removed.")
    modifications: list[FileChange] = Field(..., description="List of files modified.")

class GenerateChangeset(WorkflowNodeProtocol):
    """
    Generate a changeset.
    """

    def __call__(self, state: dict) -> dict:
        """
        Generate a changeset.

        Args:
            state (dict): State dictionary.
        """
        
        if "goal" not in state:
            raise ValueError("Goal not found in state.")

        prompt_template = PullRequestPrompt()
        prompt = prompt_template.format(goal=state["goal"],
                                          rules=state["project_rules"],
                                          tree=state["directory_tree"],
                                          content=["source_code"])
        
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")
        structured_llm = llm.with_structured_output(Changeset)

        print("\nGenerating changeset. This may take a minute...\n")

        with get_openai_callback() as cb:
            changeset = structured_llm.invoke([prompt])

        print(f"{changeset.summary}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")

        return {"changeset": changeset, "progress": "Changeset generated."}
    