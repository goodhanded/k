import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol
from adapters.prompts import CodeAdvicePrompt

class GenerateCodeAdvice(WorkflowNodeProtocol):
    """
    Generate a changeset.
    """

    def __call__(self, state: dict) -> dict:
        """
        Generate a changeset.

        Args:
            state (dict): State dictionary.
        """
        
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        prompt_template = CodeAdvicePrompt()
        prompt = prompt_template.format(prompt=state["prompt"],
                                        tree=state["directory_tree"],
                                        source_code=["source_code"])
        
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")

        print("\nGenerating changeset. This may take a minute...\n")

        with get_openai_callback() as cb:
            advice = llm.invoke([prompt])

        print(f"{advice}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")

        return {"advice": advice, "progress": "Advice generated."}
    