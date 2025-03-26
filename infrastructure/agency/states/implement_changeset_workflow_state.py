from typing import TypedDict


class ImplementChangesetWorkflowState(TypedDict):
    """
    Workflow state for the implement changeset workflow.

    Fields:
      - changeset: The structured changeset object generated from the LLM.
      - project_path: The absolute path to the project's root directory.
      - verbose: Boolean flag indicating whether verbose mode is enabled.
    """
    changeset: dict
    project_path: str
    verbose: bool
