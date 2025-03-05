import os
import json
from application.agency.protocols.workflow_node import WorkflowNodeProtocol


class ParseUserStories(WorkflowNodeProtocol):
    """
    Workflow node that parses generated user stories and writes them to .k/user_stories.txt.
    """
    def __call__(self, state: dict) -> dict:
        if "user_stories" not in state or not state["user_stories"]:
            return {"progress": "No user stories to parse."}
        if "project_path" not in state:
            raise ValueError("project_path is required in the state dictionary")

        # Convert the structured user stories to a formatted JSON string for now.
        output = json.dumps(state["user_stories"].dict(), indent=2)
        k_dir = state["project_path"]

        file_path = os.path.join(k_dir, "user_stories.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nUser stories written to {file_path}")
        return {"progress": "User stories parsed and written to .k/user_stories.txt."}
