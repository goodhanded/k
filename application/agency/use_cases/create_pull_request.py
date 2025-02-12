import sys
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import WorkflowProtocol
    from application.filesystem import ClipboardProtocol


class CreatePullRequestUseCase:
    """
    Use case for creating a pull request by invoking the pull request workflow.
    It initializes a new state dictionary with the provided prompt as the goal,
    and passes it to the workflow's run method. Additional flags support reading the prompt from stdin,
    copying the generated pull request prompt to the clipboard instead of invoking the LLM, and token count confirmation.
    """

    def __init__(self, clipboard_service: 'ClipboardProtocol', workflow: 'WorkflowProtocol') -> None:
        self.clipboard_service = clipboard_service
        self.workflow = workflow

    def _load_pattern(self, file_path: str) -> str:
        """
        Helper method to load a pattern string from a text file.
        Each rule is on its own line; this method concatenates them using the | delimiter.
        Returns the concatenated pattern if the file exists and is not empty.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                rules = [line.strip() for line in lines if line.strip()]
                return "|".join(rules) if rules else ""
        except FileNotFoundError:
            return ""

    def _generate_pr_prompt(self, goal: str) -> str:
        """
        Generates the pull request prompt using project information.
        It loads include/exclude rules, project rules, the file collection tree, and uses the PullRequestPrompt template
        to format the prompt.
        """
        from domain.filesystem import FileCollection
        from adapters.prompts.pull_request_prompt import PullRequestPrompt

        current_dir = os.getcwd()
        include_rule = self._load_pattern(os.path.join(".k", "includes.txt"))
        exclude_rule = self._load_pattern(os.path.join(".k", "excludes.txt"))
        file_collection = FileCollection.from_path(current_dir, include_rule, exclude_rule)

        try:
            with open(os.path.join(".k", "rules.txt"), "r", encoding="utf-8") as f:
                rules_text = f.read()
        except FileNotFoundError:
            rules_text = ""

        directory_tree = file_collection.tree()
        content_md = file_collection.to_markdown()
        prompt_template = PullRequestPrompt()
        return prompt_template.format(goal=goal, rules=rules_text, tree=directory_tree, content=content_md)

    def execute(self,
                prompt: str = None,
                stdin: bool = False,
                paste: bool = False,
                copy: bool = False,
                confirm: bool = False) -> None:
        """
        Executes the pull request creation process.

        Parameters:
          - prompt: The prompt text to generate the pull request changes.
          - stdin: If True, read the prompt from standard input.
          - clipboard: If True, generate and copy the PR prompt to the clipboard instead of invoking the LLM.
          - confirm: If True, display the token count and require user confirmation before proceeding.
        """
        if stdin:
            prompt = sys.stdin.read()
        elif paste:
            prompt = self.clipboard_service.get()
        if not prompt:
            print("No prompt provided. Aborting pull request creation.")
            return

        if copy or confirm:
            pr_prompt = self._generate_pr_prompt(prompt)
            if confirm:
                from infrastructure.util.token_counter import TokenCounter
                token_count = TokenCounter().count_tokens(pr_prompt)
                print(f"Estimated input tokens: {token_count}")
                user_input = input("Proceed with sending prompt? (y/n): ").strip().lower()
                if user_input != 'y':
                    print("Operation cancelled.")
                    return
            if copy:
                try:
                    self.clipboard_service.set(pr_prompt)
                    print("PR prompt copied to clipboard. No LLM invocation performed.")
                except Exception as e:
                    print(f"Failed to copy to clipboard: {e}")
                return

        # Proceed with executing the pull request workflow
        state = {"goal": prompt}
        self.workflow.run(state)
