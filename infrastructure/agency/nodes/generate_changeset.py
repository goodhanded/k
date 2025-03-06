from pydantic import BaseModel, Field
import os
from langchain_core.language_models import BaseChatModel
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
    def __init__(self, chat_model: BaseChatModel, clipboard: ClipboardProtocol, prompt: TemplateProtocol, callback: callable = None) -> None:
        self.chat_model = chat_model
        self.clipboard = clipboard
        self.prompt = prompt
        self.callback = callback

    def __call__(self, state: dict) -> dict:
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        
        memory_text = ""
        if state.get("followup", False) and "project_path" in state:
            mem_file = os.path.join(state["project_path"], ".k", "memory.txt")
            if os.path.exists(mem_file):
                with open(mem_file, "r", encoding="utf-8") as f:
                    memory_text = f.read()
        
        prompt_text = self.prompt.format(
            goal=state["goal"],
            rules=state.get("project_rules", ""),
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", ""),
            memory=memory_text
        )
        
        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt_text)
                print("\nPR prompt copied to clipboard. No LLM invocation performed.\n")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "PR prompt copied to clipboard."}
        
        structured_llm = self.chat_model.with_structured_output(Changeset)
        
        print("\nGenerating changeset. This may take a minute...\n")
        
        if self.callback:
            with self.callback() as cb:
                changeset = structured_llm.invoke([prompt_text])
            
            print(f"Input Tokens: {cb.prompt_tokens}")
            print(f"Output Tokens: {cb.completion_tokens}")
            print(f"Total: {cb.total_tokens}")
            print(f"Cost: {cb.total_cost}\n")
        else:
            changeset = structured_llm.invoke([prompt_text])
        
        print(f"{changeset.summary}\n")
        
        return {"changeset": changeset, "changeset_prompt": prompt_text, "progress": "Changeset generated."}
