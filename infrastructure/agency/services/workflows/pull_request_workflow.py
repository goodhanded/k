from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from application.agency import WorkflowProtocol, PromptGeneratorProtocol
from application.filesystem import ClipboardProtocol
from application.util import TokenCounterProtocol
from domain.filesystem import FileCollection
import os
from typing import Optional

class FileChange(BaseModel):
    path: str = Field(..., description="Relative path to the file within the project.")
    content: Optional[str] = Field(None, description="Content of the file. Include the ENTIRE file content, not just the changes. Don't forget imports, etc.")

class Response(BaseModel):
    summary: str = Field(..., description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: list[FileChange] = Field(..., description="List of files added.")
    removals: list[FileChange] = Field(..., description="List of files removed.")
    modifications: list[FileChange] = Field(..., description="List of files modified.")

class PullRequestWorkflow(WorkflowProtocol):
    def __init__(
        self,
        prompt_generator: PromptGeneratorProtocol,
        clipboard: ClipboardProtocol,
        token_counter: TokenCounterProtocol
    ) -> None:
        print(f"Initializing PR Agent with LLM model: o3-mini")
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")
        self.generator = prompt_generator
        self.llm = llm.with_structured_output(Response)
        self.project_path = os.getcwd()
        self.include_rule = self._load_pattern(os.path.join(".k", "includes.txt")) or ""
        self.exclude_rule = self._load_pattern(os.path.join(".k", "excludes.txt")) or ""

        self.clipboard = clipboard
        self.token_counter = token_counter

        self.name = "PR Agent"
        self.model = "o3-mini"

    def _load_pattern(self, file_path: str) -> Optional[str]:
        """
        Helper method to load pattern string from a text file.
        Each rule is on its own line; this method concatenates them using the | delimiter.
        Returns the concatenated pattern if file exists and is not empty, otherwise None.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                rules = [line.strip() for line in lines if line.strip()]
                return "|".join(rules) if rules else None
        except FileNotFoundError:
            return None

    def _load_rules(self) -> str:
        try:
            with open(os.path.join(".k", "rules.txt"), "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _resolve_path(self, relative_path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.project_path, relative_path))
        if not full_path.startswith(os.path.abspath(self.project_path)):
            raise ValueError(f"Unauthorized file path modification attempt: {relative_path}")
        return full_path

    def invoke(self, prompt: str, clipboard: bool = False, confirm: bool = False):
        file_collection = FileCollection.from_path(self.project_path, self.include_rule, self.exclude_rule)
        rules = self._load_rules()
        tree = file_collection.tree()
        print(tree)
        request = self.generator.generate("pr", goal=prompt, rules=rules, tree=tree, content=file_collection.to_markdown())

        # Calculate token count using injected token_counter
        token_count = self.token_counter.count_tokens(request)
        if confirm:
            print(f"Estimated input tokens: {token_count}")
            user_input = input("Proceed with sending prompt? (y/n): ").strip().lower()
            if user_input != 'y':
                print("Operation cancelled.")
                return

        if clipboard:
            self.clipboard.set(request)
            print("PR prompt copied to clipboard. No LLM invocation performed.")
            return

        print("\nSending request. This will take a few...\n")
        response = self.llm.invoke([request])

        for file_change in response.additions + response.modifications:
            abs_path = self._resolve_path(file_change.path)
            directory = os.path.dirname(abs_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(abs_path, 'w') as f:
                print(f"Writing to {abs_path}")
                f.write(file_change.content)
        
        for file_change in response.removals:
            abs_path = self._resolve_path(file_change.path)
            if os.path.exists(abs_path):
                print(f"Removing {abs_path}")
                os.remove(abs_path)
            else:
                print(f"File {abs_path} does not exist, cannot remove.")

        print(f"\nSummary: {response.summary}\n")
