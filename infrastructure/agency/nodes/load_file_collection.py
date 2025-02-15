from application.agency import WorkflowNodeProtocol
from domain.filesystem import FileCollection

# Workflow Node: LoadFileCollection
# This node constructs a collection of project files based on the current working directory,
# applying the inclusion and exclusion patterns provided in the state.
class LoadFileCollection(WorkflowNodeProtocol):
    """
    Workflow node that loads a collection of files from the current project.

    It utilizes the project's file path and include/exclude rules from the workflow state
    to create a FileCollection, which is then used in later processing steps.
    """

    def __call__(self, state: dict) -> dict:
        """
        Load the file collection from the project directory.

        Requires 'project_path', 'include_rules', and 'exclude_rules' in state.
        Returns:
            dict: Contains 'file_collection' with a FileCollection instance and a progress message.
        """
        if "project_path" not in state:
            raise ValueError("project_path is required in the state dictionary")
        if "include_rules" not in state:
            raise ValueError("include_rules is required in the state dictionary")
        if "exclude_rules" not in state:
            raise ValueError("exclude_rules is required in the state dictionary")
        
        file_collection = FileCollection.from_path(state["project_path"], state["include_rules"], state["exclude_rules"])

        return {"file_collection": file_collection, "progress": "File collection loaded."}
