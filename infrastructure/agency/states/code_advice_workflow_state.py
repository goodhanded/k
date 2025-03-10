from typing import TypedDict

from domain.filesystem.entities.document_collection import DocumentCollection

class CodeAdviceWorkflowState(TypedDict):
    """
    Workflow state for the pull request workflow.

    Fields:
      - advice: The generated advice.
      - directory_tree: A text representation of the directory tree.
      - exclude_rules: The exclude pattern string.
      - file_collection: The file collection (DocumentCollection) loaded from the project.
      - goal: The workflow goal string.
      - include_rules: The include pattern string.
      - project_path: The absolute project path.
      - source_code: Source code.
      - tests_passed: Boolean flag indicating whether tests passed.
    """
    advice: str
    copy_prompt: bool
    directory_tree: str
    exclude_rules: str
    file_collection: DocumentCollection
    followup: bool
    include_override: str
    include_rules: str
    project_path: str
    prompt: str
    source_code: str
    verbose: bool