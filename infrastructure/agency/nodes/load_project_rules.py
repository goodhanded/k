import os

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

# Workflow Node: LoadProjectRules
# This node loads project-specific guidelines and rules from the .k/rules.txt file,
# allowing the workflow to incorporate project conventions or constraints.
class LoadProjectRules(WorkflowNodeProtocol):
    """
    Workflow node that loads project rules from the '.k/rules.txt' file.

    The loaded rules can be used to guide subsequent operations in the workflow.
    """
    def __call__(self, state: dict) -> dict:
        """
        Load and return project rules from .k/rules.txt.

        Returns:
            dict: Contains 'project_rules' with the content of rules.txt and a progress message.
        """

        return {"project_rules": self._load_rules(), "progress": "Project rules loaded."}
    
    def _load_rules(self) -> str:
        """
        Reads the project rules from the .k/rules.txt file.
        If the file is not found, returns an empty string.
        """
        try:
            with open(os.path.join(".k", "rules.txt"), "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""
