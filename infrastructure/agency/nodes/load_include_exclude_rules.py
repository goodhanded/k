import os

from typing import Optional

from application.agency import WorkflowNodeProtocol

class LoadIncludeExcludeRules(WorkflowNodeProtocol):
    """
    Load include rules.
    """

    def __call__(self, state: dict) -> dict:
        """
        Load include rules.

        Args:
            state (dict): State dictionary.
        """
        
        include_rules = self._load_pattern(os.path.join(".k", "includes.txt")) or ""
        exclude_rules = self._load_pattern(os.path.join(".k", "excludes.txt")) or ""

        return {"include_rules": include_rules, "exclude_rules": exclude_rules, "progress": "Include and exclude rules loaded."}
    
    def _load_pattern(self, file_path: str) -> Optional[str]:
        """
        Helper method to load pattern string from a text file.
        Each rule is on its own line; this method concatenates them using the | delimiter.
        Returns the concatenated pattern if file exists and is not empty, otherwise None.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                rules = [line.strip() for line in lines if line.strip()]
                return "|".join(rules) if rules else None
        except FileNotFoundError:
            return None