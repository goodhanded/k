import os
import json
from application.agency import WorkflowNodeProtocol


class ParseUserStories(WorkflowNodeProtocol):
    """
    Workflow node that parses generated user stories and writes them to .k/user_stories.txt.
    """
    def __call__(self, state: dict) -> dict:
        if "user_stories" not in state or not state["user_stories"]:
            return {"progress": "No user stories to parse."}

        # Convert the structured user stories to a formatted JSON string for now.
        output = json.dumps(state["user_stories"].dict(), indent=2)
        k_dir = os.path.join(os.getcwd(), ".k")
        if not os.path.exists(k_dir):
            os.makedirs(k_dir)
        file_path = os.path.join(k_dir, "user_stories.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nUser stories written to {file_path}")
        return {"progress": "User stories parsed and written to .k/user_stories.txt."}
