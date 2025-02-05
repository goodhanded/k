import unittest
from application.agency.use_cases.generate_prompt import GeneratePromptUseCase


class DummyClipboard:
    def __init__(self) -> None:
        self.content = ""

    def get(self) -> str:
        return self.content

    def set(self, content: str) -> None:
        self.content = content


class DummyPromptGenerator:
    def generate(self, template_name: str, **template_vars) -> str:
        return f"Generated prompt for {template_name} with {template_vars}"


class TestGeneratePromptUseCase(unittest.TestCase):
    def test_execute(self) -> None:
        clipboard = DummyClipboard()
        generator = DummyPromptGenerator()
        use_case = GeneratePromptUseCase(clipboard=clipboard, prompt_generator=generator)
        use_case.execute("dummy_template", key="value")
        self.assertIn("dummy_template", clipboard.content)
        self.assertIn("key", clipboard.content)
        self.assertIn("value", clipboard.content)


if __name__ == '__main__':
    unittest.main()
