import os
import unittest

from infrastructure.agency.services.workflows.code_review_workflow import CodeReviewWorkflow
from application.agency import PromptGeneratorProtocol
from application.util import TokenCounterProtocol
from domain.filesystem import FileCollection


class DummyPromptGenerator(PromptGeneratorProtocol):
    def generate(self, template_name: str, **template_vars) -> str:
        # Return a dummy prompt including provided information for testing
        return f"Dummy prompt with tree: {template_vars.get('tree')} and content length: {len(template_vars.get('content', ''))}"


class DummyTokenCounter(TokenCounterProtocol):
    def count_tokens(self, text: str) -> int:
        return len(text.split())


class DummyLLM:
    def invoke(self, prompts):
        return "Dummy LLM response: Code looks good."


class DummyFileCollection:
    @staticmethod
    def from_path(path, inc, exc):
        class DummyCollection:
            def tree(self):
                return "Dummy tree"
            def to_markdown(self):
                return "Dummy markdown content"
        return DummyCollection()


# Patch FileCollection.from_path to return a dummy collection
original_from_path = FileCollection.from_path
FileCollection.from_path = lambda path, inc=None, exc=None: DummyFileCollection.from_path(path, inc, exc)


class TestCodeReviewWorkflow(unittest.TestCase):
    def test_invoke(self):
        workflow = CodeReviewWorkflow(DummyPromptGenerator(), DummyTokenCounter())
        # Patch the llm attribute with DummyLLM to simulate a response
        workflow.llm = DummyLLM()
        response = workflow.invoke("Please review my code.", confirm=False)
        self.assertIn("Dummy LLM response", response)


if __name__ == "__main__":
    unittest.main()
