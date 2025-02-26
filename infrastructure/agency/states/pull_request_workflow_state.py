from typing import TypedDict
from domain.filesystem.entities.document_collection import DocumentCollection


class PullRequestWorkflowState(TypedDict):
    """
    Workflow state for the pull request workflow.

    Fields:
      - goal: The workflow goal string.
      - project_path: The absolute project path.
      - include_rules: The include pattern string.
      - exclude_rules: The exclude pattern string.
      - project_rules: The project-specific rules (from .k/rules.txt).
      - file_collection: The file collection (DocumentCollection) loaded from the project.
      - directory_tree: A text representation of the directory tree.
      - source_code: Source code.
      - changeset: The generated changeset (structured as a dict).
      - tests_passed: Boolean flag indicating whether tests passed.
      - copy_prompt: Boolean flag indicating if the generated prompt should be copied to the clipboard instead of invoking the LLM.
    """
    goal: str
    project_path: str
    include_rules: str
    exclude_rules: str
    project_rules: str
    file_collection: DocumentCollection
    directory_tree: str
    source_code: str
    changeset: dict
    tests_passed: bool
    copy_prompt: bool
    print_tree: bool
