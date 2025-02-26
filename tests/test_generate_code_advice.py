import pytest

from infrastructure.agency.nodes.generate_code_advice import GenerateCodeAdvice


class FakeChatModelAdvice:
    def invoke(self, inputs):
        # Return a dummy response object with a 'content' attribute
        class FakeResponse:
            content = "Advice: refactor for performance."
        return FakeResponse()


class FakeClipboard:
    def __init__(self):
        self.content = None

    def get(self):
        return self.content

    def set(self, content):
        self.content = content


class FakePromptAdvice:
    def format(self, **kwargs):
        # Construct a simple prompt string by combining provided values
        prompt_text = kwargs.get("prompt", "")
        tree = kwargs.get("tree", "")
        source_code = kwargs.get("source_code", "")
        return f"Advice prompt: {prompt_text}; Tree: {tree}; Source: {source_code}"


def test_generate_code_advice_normal():
    chat_model = FakeChatModelAdvice()
    clipboard = FakeClipboard()
    prompt = FakePromptAdvice()
    node = GenerateCodeAdvice(chat_model=chat_model, clipboard=clipboard, prompt=prompt, callback=None)

    state = {
        "prompt": "Refactor authentication module",
        "directory_tree": "Tree representation",
        "source_code": "def foo(): pass"
    }

    result = node(state)
    assert result["progress"] == "Advice generated."
    assert result["advice"] == "Advice: refactor for performance."


def test_generate_code_advice_missing_prompt():
    chat_model = FakeChatModelAdvice()
    clipboard = FakeClipboard()
    prompt = FakePromptAdvice()
    node = GenerateCodeAdvice(chat_model=chat_model, clipboard=clipboard, prompt=prompt, callback=None)

    state = {
        # "prompt" is intentionally missing to trigger error
        "directory_tree": "Tree",
        "source_code": "Source"
    }

    with pytest.raises(ValueError):
        node(state)
