from langchain_community.callbacks.manager import get_openai_callback
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.templating.protocols.template import TemplateProtocol
from application.filesystem.protocols.clipboard import ClipboardProtocol
from langchain_core.language_models import BaseChatModel


class GenerateCodeAdvice(WorkflowNodeProtocol):
    def __init__(self, chat_model: BaseChatModel, clipboard: ClipboardProtocol, prompt: TemplateProtocol, callback: callable = None) -> None:
        self.chat_model = chat_model
        self.clipboard = clipboard
        self.prompt = prompt
        self.callback = callback

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        prompt = self.prompt.format(
            prompt=state["prompt"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )

        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt)
                print("Code Advice prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "PR prompt copied to clipboard."}

        print("\nGenerating advice. This may take a minute...\n")

        if self.callback:
            with self.callback() as cb:
                response = self.chat_model.invoke([prompt])
            
            print(f"Input Tokens: {cb.prompt_tokens}")
            print(f"Output Tokens: {cb.completion_tokens}")
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Cost: {cb.total_cost}\n")

        else:
            response = self.chat_model.invoke([prompt])
        
        advice = response.content
        print(f"{advice}\n")
        
        return {"advice": advice, "progress": "Advice generated."}
