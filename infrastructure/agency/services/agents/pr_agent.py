import os
from domain.filesystem import FileCollection
from application.agency import AgentProtocol, ToolProtocol, PromptGeneratorProtocol
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict, Optional

import pyperclip

PR_PROMPT_TEMPLATE = "pr"
LLM_MODEL = "o3-mini"

class FileChange(BaseModel):
    path: str = Field(description="Relative path to the file within the project.")
    content: Optional[str] = Field(None, description="Content of the file. Include the ENTIRE file content, not just the changes. Don't forget imports, etc.")

class Response(BaseModel):
    summary: str = Field(description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: List[FileChange] = Field(description="List of files added.")
    removals: List[FileChange] = Field(description="List of files removed.")
    modifications: List[FileChange] = Field(description="List of files modified.")

class PRAgent(AgentProtocol):
    def __init__(self, prompt_generator: PromptGeneratorProtocol,
                 include_rule: Optional[str] = None,
                 exclude_rule: Optional[str] = None,
                 exclude_gitignore: bool = False):

        print(f"Initializing PR Agent with LLM model: {LLM_MODEL}")

        llm = ChatOpenAI(model=LLM_MODEL, reasoning_effort="high")

        self.generator = prompt_generator
        self.llm = llm.with_structured_output(Response)
        self.project_path = os.getcwd()
        self.include_rule = include_rule

        if exclude_gitignore:
            self.exclude_rule = self.load_gitignore_patterns() + (f"|{exclude_rule}" if exclude_rule else "")
        else:
            self.exclude_rule = exclude_rule

        self.name = "PR Agent"
        self.model = LLM_MODEL
        
    def load_gitignore_patterns(self):
        # Read .gitignore file and construct a rule using the format "pattern1|pattern2|..."
        ignore_rule = ""
        try:
            with open(".gitignore") as f:
                ignore_rule = "|".join([line.strip() for line in f if not line.startswith("#")])
        except FileNotFoundError:
            pass

        # Append common ignore patterns
        ignore_rule += "|.git|.vscode|__pycache__|venv|node_modules|dist|build"

        return ignore_rule
    
    def _resolve_path(self, relative_path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.project_path, relative_path))
        if not full_path.startswith(os.path.abspath(self.project_path)):
            raise ValueError(f"Unauthorized file path modification attempt: {relative_path}")
        return full_path

    def invoke(self, prompt: str, clipboard: bool = False):
        file_collection = FileCollection.from_path(self.project_path, self.include_rule, self.exclude_rule)
        tree = file_collection.tree()
        request = self.generator.generate(PR_PROMPT_TEMPLATE, goal=prompt, tree=tree, content=file_collection.to_markdown())

        if clipboard:
            # Send the generated prompt to the clipboard instead of invoking the LLM
            from infrastructure.pyperclip import Pyperclip
            clipboard_client = Pyperclip()
            clipboard_client.set(request)
            print("PR prompt copied to clipboard. No LLM invocation performed.")
            return

        print("Invoking LLM...")
        response = self.llm.invoke([request])

        # For each file change, update the filesystem
        for file_change in response.additions + response.modifications:
            abs_path = self._resolve_path(file_change.path)
            directory = os.path.dirname(abs_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(abs_path, 'w') as f:
                print(f"Writing to {abs_path}")
                f.write(file_change.content)
        
        # For each file removal, delete the file
        for file_change in response.removals:
            abs_path = self._resolve_path(file_change.path)
            if os.path.exists(abs_path):
                print(f"Removing {abs_path}")
                os.remove(abs_path)
            else:
                print(f"File {abs_path} does not exist, cannot remove.")

        print(f"Summary: {response.summary}")

    def add_tools(self, tools: list[ToolProtocol]):
        pass
    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'
