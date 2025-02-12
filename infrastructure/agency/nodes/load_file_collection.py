from application.agency import WorkflowNodeProtocol
from domain.filesystem import FileCollection

class LoadFileCollection(WorkflowNodeProtocol):
    """
    Load file collection for the current project.
    """

    def __call__(self, state: dict) -> dict:
        """
        Load the file collection for the current project.

        Args:
            state (dict): State dictionary.
        """

        if "project_path" not in state:
            raise ValueError("project_path is required in the state dictionary")
        if "include_rules" not in state:
            raise ValueError("include_rules is required in the state dictionary")
        if "exclude_rules" not in state:
            raise ValueError("exclude_rules is required in the state dictionary")
        
        file_collection = FileCollection.from_path(state["project_path"], state["include_rules"], state["exclude_rules"])

        return {"file_collection": file_collection, "progress": "File collection loaded."}
