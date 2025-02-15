import unittest
from unittest.mock import patch
from infrastructure.agency.nodes.generate_changeset import GenerateChangeset, Changeset, FileChange


class DummyClipboard:
    def __init__(self):
        self.content = ""

    def get(self):
        return self.content

    def set(self, content: str):
        self.content = content


class DummyCallback:
    prompt_tokens = 10
    completion_tokens = 5
    total_tokens = 15
    total_cost = 0.01

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class DummyLLM:
    def __init__(self, *args, **kwargs):
        pass

    def with_structured_output(self, output_model):
        return self

    def invoke(self, prompts):
        return Changeset(summary="Test summary", additions=[], removals=[], modifications=[])


class DummyPullRequestPrompt:
    def format(self, **kwargs):
        return "Formatted PR prompt"


class TestGenerateChangeset(unittest.TestCase):
    @patch("infrastructure.agency.nodes.generate_changeset.get_openai_callback", return_value=DummyCallback())
    @patch("infrastructure.agency.nodes.generate_changeset.ChatOpenAI", new=DummyLLM)
    def test_generate_changeset_execute_llm(self, mock_callback):
        dummy_clipboard = DummyClipboard()
        node = GenerateChangeset(clipboard=dummy_clipboard, pr_prompt=DummyPullRequestPrompt(), model="dummy-model")
        state = {
            "goal": "dummy goal",
            "project_rules": "dummy rules",
            "directory_tree": "dummy tree",
            "source_code": "dummy source",
            "confirmation_required": False,
            "copy_prompt": False
        }
        result = node(state)
        self.assertIn("changeset", result)
        self.assertIsNotNone(result["changeset"])
        self.assertEqual(result["changeset"].summary, "Test summary")
        self.assertEqual(result["progress"], "Changeset generated.")

    @patch("builtins.input", return_value="irrelevant")
    def test_generate_changeset_copy_prompt(self, mock_input):
        dummy_clipboard = DummyClipboard()
        node = GenerateChangeset(clipboard=dummy_clipboard, pr_prompt=DummyPullRequestPrompt(), model="dummy-model")
        state = {
            "goal": "dummy goal copy",
            "project_rules": "dummy rules",
            "directory_tree": "dummy tree",
            "source_code": "dummy source",
            "copy_prompt": True
        }
        result = node(state)
        self.assertIsNone(result["changeset"])
        self.assertEqual(result["progress"], "PR prompt copied to clipboard.")
        self.assertEqual(dummy_clipboard.content, "Formatted PR prompt")


if __name__ == '__main__':
    unittest.main()
