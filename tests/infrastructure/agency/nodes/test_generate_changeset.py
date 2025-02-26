import unittest
from unittest.mock import patch

from infrastructure.agency.nodes.generate_changeset import GenerateChangeset, Changeset, FileChange


class DummyClipboard:
    def __init__(self):
        self.content = ""
    def get(self):
        return self.content
    def set(self, content):
        self.content = content


class DummyPullRequestPrompt:
    def format(self, **kwargs):
        # Return a dummy prompt that includes the goal
        return "dummy prompt: " + kwargs.get("goal", "")


class DummyStructuredLLM:
    def invoke(self, prompts):
        # Return a dummy Changeset instance
        dummy_changeset = Changeset(
            summary="Dummy changeset summary",
            additions=[FileChange(path="added.txt", content="Added dummy")],
            removals=[],
            modifications=[]
        )
        return dummy_changeset


class DummyChatModel:
    def with_structured_output(self, structured_type):
        return DummyStructuredLLM()


class TestGenerateChangeset(unittest.TestCase):
    @patch("builtins.input", return_value="irrelevant")
    def test_generate_changeset_copy_prompt(self, mock_input):
        dummy_clipboard = DummyClipboard()
        dummy_prompt = DummyPullRequestPrompt()
        dummy_chat = DummyChatModel()
        # Note: use 'chat_model' keyword instead of 'model'
        node = GenerateChangeset(chat_model=dummy_chat, clipboard=dummy_clipboard, pr_prompt=dummy_prompt)
        state = {
            "goal": "Test goal",
            "copy_prompt": True,
            "directory_tree": "",
            "source_code": ""
        }
        result = node(state)
        self.assertIn("PR prompt copied to clipboard", result.get("progress", ""))

    def test_generate_changeset_execute_llm(self):
        dummy_clipboard = DummyClipboard()
        dummy_prompt = DummyPullRequestPrompt()
        dummy_chat = DummyChatModel()
        node = GenerateChangeset(chat_model=dummy_chat, clipboard=dummy_clipboard, pr_prompt=dummy_prompt)
        state = {
            "goal": "Test goal",
            "copy_prompt": False,
            "directory_tree": "",
            "source_code": ""
        }
        result = node(state)
        changeset = result.get("changeset")
        self.assertIsNotNone(changeset)
        self.assertEqual(changeset.summary, "Dummy changeset summary")


if __name__ == "__main__":
    unittest.main()