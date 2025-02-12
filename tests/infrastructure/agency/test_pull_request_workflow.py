import os
import sys
import tempfile
import unittest

from infrastructure.agency import PullRequestWorkflow

# Dummy classes to simulate dependencies

class DummyGenerator:
    def __init__(self):
        self.call_args = None

    def generate(self, template_name: str, **kwargs) -> str:
        self.call_args = kwargs
        return "dummy request"

class DummyTokenCounter:
    def count_tokens(self, text: str) -> int:
        return 10

class DummyLLM:
    def invoke(self, requests):
        class DummyResponse:
            additions = []
            modifications = []
            removals = []
            summary = "dummy summary"
        return DummyResponse()

class DummyClipboard:
    def __init__(self, content=""):
        self.content = content

    def get(self) -> str:
        return self.content

    def set(self, content: str):
        self.content = content

# Dummy file collection to avoid filesystem dependency
class DummyFileCollection:
    def tree(self):
        return "dummy tree"

    def to_markdown(self):
        return "dummy markdown"

# Patch FileCollection.from_path for testing
from domain.filesystem.entities.file_collection import FileCollection

class TestPullRequestWorkflow(unittest.TestCase):
    def setUp(self):
        self.dummy_generator = DummyGenerator()
        self.dummy_token_counter = DummyTokenCounter()
        self.dummy_llm = DummyLLM()
        self.dummy_clipboard = DummyClipboard("input from clipboard")

        self.workflow = PullRequestWorkflow(prompt_generator=self.dummy_generator,
                                            clipboard=self.dummy_clipboard,
                                            token_counter=self.dummy_token_counter)
        # Override attributes requiring filesystem access
        self.workflow.project_path = tempfile.mkdtemp()
        self.workflow.include_rule = ""
        self.workflow.exclude_rule = ""
        self.workflow._load_rules = lambda: "dummy rules"
        self.workflow.llm = self.dummy_llm

        # Monkey-patch FileCollection.from_path to return a dummy instance
        self.original_from_path = FileCollection.from_path
        FileCollection.from_path = lambda path, include_rule, exclude_rule: DummyFileCollection()

    def tearDown(self):
        FileCollection.from_path = self.original_from_path

    def test_invoke_with_paste(self):
        # When --paste is True, the prompt should be read from the clipboard
        self.workflow.invoke(prompt="ignored", paste=True, stdin=False, clipboard=False, confirm=False)
        self.assertIsNotNone(self.dummy_generator.call_args)
        self.assertEqual(self.dummy_generator.call_args.get("goal"), "input from clipboard")

    def test_invoke_without_paste(self):
        # When paste is False, the provided prompt is used
        self.workflow.invoke(prompt="direct input", paste=False, stdin=False, clipboard=False, confirm=False)
        self.assertIsNotNone(self.dummy_generator.call_args)
        self.assertEqual(self.dummy_generator.call_args.get("goal"), "direct input")

if __name__ == '__main__':
    unittest.main()
