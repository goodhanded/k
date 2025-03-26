import os
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.templating.protocols.template import TemplateProtocol
from application.filesystem.protocols.clipboard import ClipboardProtocol
from langchain.chat_models import init_chat_model


class GenerateCodeAdvice(WorkflowNodeProtocol):
    def __init__(self, clipboard: ClipboardProtocol, prompt: TemplateProtocol, model_id: str, model_config: dict = None) -> None:
        self.chat_model = init_chat_model(model_id, **(model_config or {}))
        self.clipboard = clipboard
        self.prompt = prompt

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        memory_text = ""
        if state.get("followup", False) and "project_path" in state:
            mem_file = os.path.join(state["project_path"], ".k", "memory.txt")
            if os.path.exists(mem_file):
                with open(mem_file, "r", encoding="utf-8") as f:
                    memory_text = f.read()

        prompt_text = self.prompt.format(
            prompt=state["prompt"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", ""),
            memory=memory_text
        )

        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt_text)
                print("Code Advice prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "Prompt copied to clipboard."}

        print("\nGenerating advice. This may take a minute...\n")

        response = self.chat_model.invoke([prompt_text])
        
        advice = response.content
        print(f"{advice}\n")
        
        return {"advice": advice, "progress": "Advice generated."}
