from typing import TypedDict
from domain.filesystem.entities.document_collection import DocumentCollection


class PullRequestWorkflowState(TypedDict):
    """
    Workflow state for the pull request workflow.
    
    Fields:
      - changeset: The generated changeset (structured as a dict).
      - copy_prompt: Boolean flag indicating if the generated prompt should be copied to the clipboard instead of invoking the LLM.
      - directory_tree: A text representation of the directory tree.
      - exclude_rules: The exclude pattern string.
      - file_collection: The file collection (DocumentCollection) loaded from the project.
      - followup: Boolean flag indicating if followup mode is active.
      - include_override: Override include patterns.
      - include_rules: The include pattern string.
      - print_tree: Boolean flag for printing the directory tree.
      - project_path: The absolute project path.
      - project_rules: The project-specific rules (from .k/rules.txt).
      - prompt: The workflow prompt string.
      - source_code: Source code.
      - tests_passed: Boolean flag indicating whether tests passed.
      - verbose: Boolean flag for verbose output.
    """
    changeset: dict
    copy_prompt: bool
    directory_tree: str
    exclude_rules: str
    file_collection: DocumentCollection
    followup: bool
    include_override: str
    include_rules: str
    print_tree: bool
    project_path: str
    project_rules: str
    prompt: str
    source_code: str
    tests_passed: bool
    verbose: bool
