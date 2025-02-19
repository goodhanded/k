from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol


class GenerateCodeAdvice(WorkflowNodeProtocol):
    def __init__(self, code_advice_prompt, model: str):
        self.code_advice_prompt = code_advice_prompt
        self.model = model

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        prompt = self.code_advice_prompt.format(
            prompt=state["prompt"],
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )

        llm = ChatOpenAI(model=self.model, reasoning_effort="high")

        print(f"Generating advice. This could take a minute...")

        with get_openai_callback() as cb:
            response = llm.invoke([prompt])
        
        advice = response.content
        print(f"{advice}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")
        
        return {"advice": advice, "progress": "Advice generated."}
