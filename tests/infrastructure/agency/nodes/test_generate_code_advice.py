import unittest
from unittest.mock import patch
from infrastructure.agency.nodes.generate_code_advice import GenerateCodeAdvice


class DummyResponse:
    def __init__(self, content):
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
    def invoke(self, prompts):
        return DummyResponse("dummy advice")


class DummyCodeAdvicePrompt:
    def format(self, **kwargs):
        return "formatted prompt"


class TestGenerateCodeAdvice(unittest.TestCase):
    @patch("infrastructure.agency.nodes.generate_code_advice.ChatOpenAI", return_value=DummyLLM())
    @patch("infrastructure.agency.nodes.generate_code_advice.get_openai_callback", return_value=DummyCallback())
    def test_generate_code_advice(self, mock_get_callback, mock_chat):
        node = GenerateCodeAdvice(DummyCodeAdvicePrompt())
        state = {
            "prompt": "Test code advice prompt",
            "directory_tree": "dummy tree",
            "source_code": "dummy source"
        }
        result = node(state)
        self.assertIn("advice", result)
        self.assertEqual(result["advice"], "dummy advice")
        self.assertEqual(result["progress"], "Advice generated.")


if __name__ == '__main__':
    unittest.main()
