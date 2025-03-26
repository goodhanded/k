import json

from application.filesystem.protocols.clipboard import ClipboardProtocol
from application.agency.protocols.workflow import WorkflowProtocol
from application.util.project_root import find_project_root

# Import the Changeset model from the generate_changeset node
from infrastructure.agency.nodes.generate_changeset import Changeset


class ImplementChangesetUseCase:
    """
    Use case for implementing a changeset that is read from the clipboard.
    
    It reads a structured changeset response from the clipboard, parses it,
    retrieves the project root, and then executes the implementation workflow.
    """
    def __init__(self, clipboard_service: ClipboardProtocol, workflow: WorkflowProtocol) -> None:
        self.clipboard_service = clipboard_service
        self.workflow = workflow

    def execute(self, verbose: bool = False) -> None:
        content: str = self.clipboard_service.get()
        if not content:
            print("No changeset content found in clipboard. Aborting implementation.")
            return

        try:
            # Expecting the clipboard content to be a JSON string representing the structured changeset
            data = json.loads(content)
        except Exception as e:
            print(f"Failed to decode clipboard content as JSON: {e}")
            return

        try:
            changeset = Changeset.parse_obj(data)
        except Exception as e:
            print(f"Failed to parse changeset: {e}")
            return

        project_path = find_project_root()
        if not project_path:
            print("Project root with .k directory not found. Please run 'k init' first.")
            return

        state = {
            "changeset": changeset,
            "project_path": project_path,
            "verbose": verbose
        }

        result = self.workflow.run(state)
        print("Implementation complete.")
