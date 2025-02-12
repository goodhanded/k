import os

from application.agency import WorkflowNodeProtocol

class LoadProjectRules(WorkflowNodeProtocol):
    """
    Load project rules from the rules.txt file in the .k directory.
    """
    def __call__(self, state: dict) -> dict:
        """
        Load project rules from the rules.txt file in the .k directory.

        Args:
            state (dict): State dictionary.
        """

        # Load directory tree
        return {"project_rules": self._load_rules(), "progress": "Project rules loaded."}
    
    def _load_rules(self) -> str:
        try:
            with open(os.path.join(".k", "rules.txt"), "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""