from typing import TypedDict

from domain.filesystem.entities.document_collection import DocumentCollection

class CodeAdviceWorkflowState(TypedDict):
    """
    Workflow state for the pull request workflow.

    Fields:
      - goal: The workflow goal string.
      - project_path: The absolute project path.
      - include_rules: The include pattern string.
      - exclude_rules: The exclude pattern string.
      - file_collection: The file collection (DocumentCollection) loaded from the project.
      - directory_tree: A text representation of the directory tree.
      - source_code: Source code.
      - advice: The generated advice.
      - tests_passed: Boolean flag indicating whether tests passed.
    """
    prompt: str
    project_path: str
    include_rules: str
    exclude_rules: str
    file_collection: DocumentCollection
    directory_tree: str
    source_code: str
    advice: str
    print_tree: bool
    include_override: str
