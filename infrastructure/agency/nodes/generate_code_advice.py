from langchain_community.callbacks.manager import get_openai_callback
from application.agency.protocols.workflow_node import WorkflowNodeProtocol
from application.templating.protocols.template import TemplateProtocol
from langchain_core.language_models import BaseChatModel


class GenerateCodeAdvice(WorkflowNodeProtocol):
    def __init__(self, chat_model: BaseChatModel, prompt: TemplateProtocol, callback: callable = None) -> None:
        self.prompt = prompt
        self.chat_model = chat_model
        self.callback = callback

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        prompt = self.prompt.format(
            prompt=state["prompt"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )

        print("\nGenerating advice. This may take a minute...\n")

        # with get_openai_callback() as cb:
        #     response = self.chat_model.invoke([prompt])

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
