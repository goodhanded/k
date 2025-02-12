from langchain_openai import ChatOpenAI
from application.agency import WorkflowProtocol, PromptGeneratorProtocol
from application.util import TokenCounterProtocol
from domain.filesystem import FileCollection
import os
from typing import Optional


class CodeReviewWorkflow(WorkflowProtocol):
    def __init__(self,
                 prompt_generator: PromptGeneratorProtocol,
                 token_counter: TokenCounterProtocol
    ) -> None:
        # Initialize LLM for code review with raw text output
        self.llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")
        self.prompt_generator = prompt_generator
        self.token_counter = token_counter
        self.project_path = os.getcwd()
        self.include_rule = self._load_pattern(os.path.join(".k", "includes.txt")) or ""
        self.exclude_rule = self._load_pattern(os.path.join(".k", "excludes.txt")) or ""

    def _load_pattern(self, file_path: str) -> Optional[str]:
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

    def run(self, prompt: str = "", confirm: bool = False):
        # Build file collection from project directory using include/exclude patterns
        file_collection = FileCollection.from_path(self.project_path, self.include_rule, self.exclude_rule)
        tree = file_collection.tree()
        generated_prompt = self.prompt_generator.generate(
            "code_review",
            tree=tree,
            content=file_collection.to_markdown()
        )
        
        token_count = self.token_counter.count_tokens(generated_prompt)
        if confirm:
            print(f"Estimated input tokens: {token_count}")
            user_input = input("Proceed with sending prompt? (y/n): ").strip().lower()
            if user_input != 'y':
                print("Operation cancelled.")
                return

        print("\nSending code review prompt...\n")
        response = self.llm.invoke([generated_prompt])
        print("\nLLM Response:\n")
        print(response.content)