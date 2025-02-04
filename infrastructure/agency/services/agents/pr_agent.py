import os
from domain.filesystem import DocumentCollection
from application.agency import AgentProtocol, ToolProtocol, PromptGeneratorProtocol
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict, Optional

import pyperclip

PR_PROMPT_TEMPLATE = "pr"
LLM_MODEL = "o3-mini"

class FileChange(BaseModel):
    path: str = Field(description="Absolute path to the file.")
    content: Optional[str] = Field(None, description="Content of the file.")

class Response(BaseModel):
    summary: str = Field(description="Descriptive summary of files added, removed, or modified. Explain what was done and why in one sentence for each file.")
    additions: List[FileChange] = Field(description="List of files added.")
    removals: List[FileChange] = Field(description="List of files removed.")
    modifications: List[FileChange] = Field(description="List of files modified.")

class PRAgent(AgentProtocol):
    def __init__(self, prompt_generator: PromptGeneratorProtocol):

        print(f"Initializing PR Agent with LLM model: {LLM_MODEL}")

        llm = ChatOpenAI(model=LLM_MODEL, reasoning_effort="high")

        self.generator = prompt_generator
        self.llm = llm.with_structured_output(Response)
        self.project_path = os.getcwd()
        self.ignore_rule = self.create_ignore_rule()

        self.name = "PR Agent"
        self.model = LLM_MODEL
        
    def create_ignore_rule(self):
        # Read .gitignore file and construct a rule using the format "pattern1|pattern2|..."
        ignore_rule = ""
        try:
            with open(".gitignore") as f:
                ignore_rule = "|".join([line.strip() for line in f if not line.startswith("#")])
        except FileNotFoundError:
            pass
        return ignore_rule
    
    def invoke(self, prompt: str):

        print(f"Running PR Agent on {self.project_path} with ignore rule: {self.ignore_rule}")
        print(f"Getting document collection from {self.project_path}")
        document_collection = DocumentCollection(self.project_path, self.ignore_rule)

        print(f"Generating prompt for PR")
        tree = document_collection.tree()
        content = document_collection.to_document().content_with_path()
        prompt = self.generator.generate(PR_PROMPT_TEMPLATE, goal=prompt, tree=tree, content=content)

        pyperclip.copy(prompt)

        print(f"Prompt copied to clipboard.")
        return

        print(f"Invoking LLM with prompt: {prompt}")
        response = self.llm.invoke([prompt])

        # For each file change, update the filesystem
        for file_change in response.additions + response.modifications:
            with open(file_change.path, 'w') as f:
                print(f"Writing to {file_change.path}")
                f.write(file_change.content)
        
        # For each file removal, delete the file
        for file_change in response.removals:
            print(f"Removing {file_change.path}")
            os.remove(file_change.path)

    def add_tools(self, tools: list[ToolProtocol]):
        pass
    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'