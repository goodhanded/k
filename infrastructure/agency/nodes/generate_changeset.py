import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from application.agency import WorkflowNodeProtocol

# Workflow Node: GenerateChangeset
# This node generates a pull request changeset by creating a prompt using the PullRequestPrompt template,
# optionally confirming token count with the user, optionally copying the prompt to clipboard instead of invoking the LLM,
# and finally invoking an LLM with structured output to produce a changeset that details file additions, removals, and modifications.


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
    A workflow node that generates a pull request changeset by orchestrating several steps:

    1) It first formats a prompt using a provided template (e.g. PullRequestPrompt), incorporating the workflow goal, 
       project rules, the directory tree, and the source code of the project.

    2) It then assesses the token usage of the prompt via a token counter to estimate LLM invocation costs, 
       and if user confirmation is required, asks the user whether to proceed.

    3) Alternatively, if the 'copy_prompt' flag is set in the state, it copies the formatted prompt to the clipboard 
       and skips LLM processing.

    4) Otherwise, it calls a language model (using ChatOpenAI) with structured output configured for a Changeset,
       prints token usage details and the summary returned, and finally injects the produced changeset back into the workflow state.

    Constructor Parameters:
      - clipboard: A clipboard service used for copying text (implements ClipboardProtocol).
      - pr_prompt: A prompt template instance (like PullRequestPrompt) used to format the changeset generation prompt.
    """
    def __init__(self, clipboard, pr_prompt):
        self.clipboard = clipboard
        self.pr_prompt = pr_prompt

    def __call__(self, state: dict) -> dict:
        """
        Generates and returns a pull request changeset based on the workflow state.

        Expected state keys:
          - 'goal': A string describing the pull request goal/intent.
          - 'project_rules' (optional): Project-specific guidelines or rules.
          - 'directory_tree' (optional): A textual representation of the project directory structure.
          - 'source_code' (optional): The aggregated source code of the project.
          - 'confirmation_required' (optional): Boolean flag whether to prompt for user confirmation based on token count.
          - 'copy_prompt' (optional): Boolean flag whether to copy the generated prompt to clipboard instead of LLM invocation.

        Process:
          1. Validates that a 'goal' exists in the state; otherwise, raises an error.
          2. Uses the provided prompt template to format a prompt with the goal, rules, directory tree, and source code.
          3. Counts the tokens in the prompt to estimate LLM usage and stores this count in the state.
          4. If confirmation is required, prints the token estimate and waits for user input; aborts if not confirmed.
          5. If the 'copy_prompt' flag is set, copies the formatted prompt to the clipboard and returns without invoking the LLM.
          6. Otherwise, instantiates a ChatOpenAI model with specified parameters and configures it for structured output of type Changeset.
          7. Invokes the LLM with the prompt while capturing token usage statistics via a callback.
          8. Prints the summarized changeset and token usage details, updates the state with the changeset, and returns a summary progress.

        Returns:
          A dictionary containing:
            - 'changeset': The generated Changeset object (or None if operation was cancelled/copied).
            - 'progress': A string message indicating the status of changeset generation.
        """
        # Verify that the essential 'goal' is provided in the state.
        if "goal" not in state:
            raise ValueError("Goal not found in state.")
        
        # Format the PR prompt by injecting the workflow goal, project rules, directory tree, and source code.
        prompt = self.pr_prompt.format(
            goal=state["goal"],
            rules=state.get("project_rules", ""),
            tree=state.get("directory_tree", ""),
            source_code=state.get("source_code", "")
        )
        
        # Estimate the number of tokens in the prompt to gauge potential LLM cost.
        from infrastructure.util.token_counter import TokenCounter
        token_counter = TokenCounter()
        token_count = token_counter.count_tokens(prompt)
        state["token_count"] = token_count
        
        # If required, ask the user to confirm proceeding with the LLM call based on token estimate.
        if state.get("confirmation_required", False):
            print(f"Estimated input tokens: {token_count}")
            user_input = input("Proceed with sending prompt? (y/n): ").strip().lower()
            if user_input != 'y':
                print("Operation cancelled by user.")
                return {"changeset": None, "progress": "Operation cancelled."}
        
        # If the option to copy the prompt is enabled, copy prompt to clipboard and skip LLM invocation.
        if state.get("copy_prompt", False):
            try:
                self.clipboard.set(prompt)
                print("PR prompt copied to clipboard. No LLM invocation performed.")
            except Exception as e:
                print(f"Failed to copy prompt to clipboard: {e}")
            return {"changeset": None, "progress": "PR prompt copied to clipboard."}
        
        # Invoke the LLM with structured output configured for Changeset.
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")
        structured_llm = llm.with_structured_output(Changeset)
        
        print("\nGenerating changeset. This may take a minute...\n")
        with get_openai_callback() as cb:
            changeset = structured_llm.invoke([prompt])
        
        # Output the changeset summary and token usage information.
        print(f"{changeset.summary}\n")
        print(f"Input Tokens: {cb.prompt_tokens}")
        print(f"Output Tokens: {cb.completion_tokens}")
        print(f"Total: {cb.total_tokens}")
        print(f"Cost: {cb.total_cost}\n")
        
        # Update the workflow state with the generated changeset and return progress.
        state["changeset"] = changeset
        return {"changeset": changeset, "progress": "Changeset generated."}
