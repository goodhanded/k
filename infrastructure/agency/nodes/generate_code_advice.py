import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol


class GenerateCodeAdvice(WorkflowNodeProtocol):
    """
    Workflow node that generates code advice by analyzing a codebase.
    
    The node expects the state dictionary to contain:
      - 'prompt': A user-provided prompt for code advice.
      - 'directory_tree': Textual representation of the project's directory structure.
      - 'source_code': The project's source code in markdown format.
    It formats a prompt using the injected CodeAdvicePrompt, calls the LLM, prints token usage, and returns the advice along with a progress message.
    """

    def __init__(self, code_advice_prompt):
        self.code_advice_prompt = code_advice_prompt

    def __call__(self, state: dict) -> dict:
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        prompt = self.code_advice_prompt.format(prompt=state["prompt"],
                                                 tree=state.get("directory_tree", ""),
                                                 source_code=state.get("source_code", ""))

        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")

        print("\nGenerating code advice. This may take a minute...\n")
        with get_openai_callback() as cb:
            response = llm.invoke([prompt])
        
        advice = response.content
        
        print(f"{advice}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")
        
        return {"advice": advice, "progress": "Advice generated."}
