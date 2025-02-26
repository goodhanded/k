import pytest

from infrastructure.agency.nodes.generate_changeset import GenerateChangeset, Changeset


class FakeChatModel:
    def with_structured_output(self, output_type):
        self.output_type = output_type
        return self

    def invoke(self, inputs):
        # Return a dummy Changeset instance
        return Changeset(
            summary="Dummy changeset summary",
            additions=[],
            removals=[],
            modifications=[]
        )


class FakeClipboard:
    def __init__(self):
        self.content = None

    def get(self):
        return self.content

    def set(self, content):
        self.content = content


class FakePrompt:
    def format(self, **kwargs):
        # For testing, simply incorporate the 'goal' value in the returned string
        goal = kwargs.get("goal", "")
        # Even if other kwargs are present, simply include them in the string for verification if needed
        project_rules = kwargs.get("project_rules", "")
        directory_tree = kwargs.get("directory_tree", "")
        source_code = kwargs.get("source_code", "")
        return f"Formatted prompt with goal: {goal}; rules: {project_rules}; tree: {directory_tree}; source: {source_code}"


def test_generate_changeset_normal():
    chat_model = FakeChatModel()
    clipboard = FakeClipboard()
    prompt = FakePrompt()
    node = GenerateChangeset(chat_model=chat_model, clipboard=clipboard, prompt=prompt, callback=None)

    state = {
        "goal": "Add new feature",
        "project_rules": "Some project rules",
        "directory_tree": "Tree representation",
        "source_code": "Some source code",
        "copy_prompt": False
    }

    result = node(state)
    assert result["progress"] == "Changeset generated."
    changeset = result["changeset"]
    assert changeset is not None
    assert changeset.summary == "Dummy changeset summary"


def test_generate_changeset_copy_prompt():
    chat_model = FakeChatModel()
    clipboard = FakeClipboard()
    prompt = FakePrompt()
    node = GenerateChangeset(chat_model=chat_model, clipboard=clipboard, prompt=prompt, callback=None)

    state = {
        "goal": "Fix bug",
        "project_rules": "Rules",
        "directory_tree": "Directory Tree",
        "source_code": "Source",
        "copy_prompt": True
    }

    result = node(state)
    # When copy_prompt is True, the node should not invoke the LLM; changeset is None
    assert result["changeset"] is None
    assert result["progress"] == "PR prompt copied to clipboard."
    expected_prompt = prompt.format(goal="Fix bug", project_rules="Rules", directory_tree="Directory Tree", source_code="Source")
    print(f"Expected prompt: {expected_prompt}")
    print(f"Actual clipboard content: {clipboard.content}")
    assert clipboard.content == expected_prompt


def test_generate_changeset_missing_goal():
    chat_model = FakeChatModel()
    clipboard = FakeClipboard()
    prompt = FakePrompt()
    node = GenerateChangeset(chat_model=chat_model, clipboard=clipboard, prompt=prompt, callback=None)

    state = {
        # "goal" is intentionally missing to test error handling
        "project_rules": "Rules",
        "directory_tree": "Tree",
        "source_code": "Source",
        "copy_prompt": False
    }

    with pytest.raises(ValueError):
        node(state)
