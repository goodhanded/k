from pydantic import BaseModel, Field
from langchain_core.language_models import BaseChatModel
from langchain_community.callbacks.manager import get_openai_callback
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.filesystem.protocols.clipboard import ClipboardProtocol
from application.templating.protocols.template import TemplateProtocol

class FileChange(BaseModel):
    path: str = Field(description="Relative path to the file within the project.")
    content: str = Field(description="Content of the file. Include the ENTIRE file content, not just the changes. Don't forget imports, etc.")

class Changeset(BaseModel):
    summary: str = Field(description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: list[FileChange] = Field(description="List of files added.")
    removals: list[FileChange] = Field(description="List of files removed.")
    modifications: list[FileChange] = Field(description="List of files modified.")

class GenerateChangeset(WorkflowNodeProtocol):
    """
    Workflow node that generates a pull request changeset.
    """
    def __init__(self, chat_model: BaseChatModel, clipboard: ClipboardProtocol, pr_prompt: TemplateProtocol, model_name: str):
        self.chat_model = chat_model
        self.clipboard = clipboard
        self.pr_prompt = pr_prompt
        self.model_name = model_name

    def __call__(self, state: dict) -> dict:
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        
        prompt = self.pr_prompt.format(
            goal=state["goal"],
            rules=state.get("project_rules", ""),
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )
        
        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt)
                print("PR prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "PR prompt copied to clipboard."}
        
        structured_llm = self.chat_model.with_structured_output(Changeset)
        
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
