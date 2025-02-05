import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from application.agency import AgentProtocol, PromptGeneratorProtocol
from application.filesystem import ClipboardProtocol
from application.util import TokenCounterProtocol
from domain.filesystem import FileCollection

# Removed old token counter import

class FileChange(BaseModel):
    path: str = Field(description="Relative path to the file within the project.")
    content: Optional[str] = Field(None, description="Content of the file. Include the ENTIRE file content, not just the changes. Don't forget imports, etc.")


class Response(BaseModel):
    summary: str = Field(description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: list[FileChange] = Field(description="List of files added.")
    removals: list[FileChange] = Field(description="List of files removed.")
    modifications: list[FileChange] = Field(description="List of files modified.")


class PRAgent(AgentProtocol):
    def __init__(
        self,
        prompt_generator: PromptGeneratorProtocol,
        clipboard: ClipboardProtocol,
        token_counter: TokenCounterProtocol,
        include_rule: Optional[str] = None,
        exclude_rule: Optional[str] = None,
        exclude_gitignore: bool = False
    ):
        print(f"Initializing PR Agent with LLM model: o3-mini")
        llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")
        self.generator = prompt_generator
        self.llm = llm.with_structured_output(Response)
        self.project_path = os.getcwd()
        self.include_rule = include_rule
        self.clipboard = clipboard
        self.token_counter = token_counter

        if exclude_gitignore:
            self.exclude_rule = self.load_gitignore_patterns() + (f"|{exclude_rule}" if exclude_rule else "")
        else:
            self.exclude_rule = exclude_rule

        self.name = "PR Agent"
        self.model = "o3-mini"

    def load_gitignore_patterns(self) -> str:
        ignore_rule = ""
        try:
            with open(".gitignore") as f:
                ignore_rule = "|".join([line.strip() for line in f if not line.startswith("#")])
        except FileNotFoundError:
            pass
        ignore_rule += "|.git|.vscode|__pycache__|venv|node_modules|dist|build"
        return ignore_rule

    def _resolve_path(self, relative_path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.project_path, relative_path))
        if not full_path.startswith(os.path.abspath(self.project_path)):
            raise ValueError(f"Unauthorized file path modification attempt: {relative_path}")
        return full_path

    def invoke(self, prompt: str, clipboard: bool = False, confirm: bool = False):
        file_collection = FileCollection.from_path(self.project_path, self.include_rule, self.exclude_rule)
        tree = file_collection.tree()
        print(tree)
        request = self.generator.generate("pr", goal=prompt, tree=tree, content=file_collection.to_markdown())

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

        print("Sending request. This will take a few...")
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
