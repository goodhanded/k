import os

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol
from adapters.prompts import CodeAdvicePrompt

# Workflow Node: GenerateCodeAdvice
# This node generates code advice by formatting a prompt using the CodeAdvicePrompt template,
# invoking a language model (ChatOpenAI) with the formatted prompt, and returning the advice.

class GenerateCodeAdvice(WorkflowNodeProtocol):
    """
    Workflow node that generates code advice by analyzing a codebase.
    
    The node expects the state dictionary to contain:
      - 'prompt': A user-provided prompt for code advice.
      - 'directory_tree': Textual representation of the project's directory structure.
      - 'source_code': The project's source code in markdown format.
    It formats a prompt, calls the LLM, prints token usage, and returns the advice along with a progress message.
    """

    def __call__(self, state: dict) -> dict:
        """
        Generates code advice by invoking an LLM with a formatted prompt.

        Steps:
          1. Validate that the 'prompt' key exists in the state.
          2. Format the prompt using the CodeAdvicePrompt template with provided state values.
          3. Initialize a ChatOpenAI model instance.
          4. Invoke the LLM with the formatted prompt while capturing token usage.
          5. Print the advice and token statistics.
          6. Return the generated advice in the state.
        """
        if "prompt" not in state:
            raise ValueError("Prompt not found in state.")

        # Format the prompt using the CodeAdvicePrompt template.
        prompt_template = CodeAdvicePrompt()
        prompt = prompt_template.format(prompt=state["prompt"],
                                        tree=state["directory_tree"],
                                        source_code=state["source_code"])
        
        # Initialize the language model with specified model and reasoning effort.
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")

        print("\nGenerating code advice. This may take a minute...\n")

        # Invoke the LLM with the formatted prompt and capture token usage via callback.
        with get_openai_callback() as cb:
            response = llm.invoke([prompt])

        advice = response.content

        # Output the advice and token statistics to the console.
        print(f"{advice}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")

        return {"advice": advice, "progress": "Advice generated."}
