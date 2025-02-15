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
    Generate a changeset node that generates the PR prompt and conditionally handles user confirmation and clipboard copying.
    """

    def __init__(self, clipboard):
        self.clipboard = clipboard

    def __call__(self, state: dict) -> dict:
        """
        Generate a changeset.

        Args:
            state (dict): State dictionary with keys:
              - goal
              - project_rules
              - directory_tree
              - source_code
              - confirmation_required (bool)
              - copy_prompt (bool)
        """
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        
        prompt_template = PullRequestPrompt()
        prompt = prompt_template.format(
            goal=state["goal"],
            rules=state.get("project_rules", ""),
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )
        
        # Token counting and confirmation if required
        from infrastructure.util.token_counter import TokenCounter
        token_counter = TokenCounter()
        token_count = token_counter.count_tokens(prompt)
        state["token_count"] = token_count
        if state.get("confirmation_required", False):
            print(f"Estimated input tokens: {token_count}")
            user_input = input("Proceed with sending prompt? (y/n): ").strip().lower()
            if user_input != 'y':
                print("Operation cancelled by user.")
                return {"changeset": None, "progress": "Operation cancelled."}
        
        # Clipboard copy functionality if requested
        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt)
                print("PR prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "PR prompt copied to clipboard."}
        
        # Proceed with LLM invocation
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
        
        state["changeset"] = changeset
        return {"changeset": changeset, "progress": "Changeset generated."}
