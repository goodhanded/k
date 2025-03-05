import os
from typing import Any, Optional

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

# Workflow Node: LoadIncludeExcludeRules
# This node loads file inclusion and exclusion rules from .k/includes.txt and .k/excludes.txt,
# concatenates each rule file's lines with a '|' delimiter, and returns the patterns.
class LoadIncludeExcludeRules(WorkflowNodeProtocol):
    """
    Workflow node that loads include and exclude patterns used to filter files in the project.

    It reads the contents of '.k/includes.txt' and '.k/excludes.txt' (if present),
    converts the list of rules into a single pattern string, and adds these to the workflow state.
    """

    def __call__(self, state: dict) -> dict:

        if "project_path" not in state:
            raise ValueError("Project path not found in state.")
        
        project_path = state["project_path"]

        if 'include_override' in state and state['include_override']:
            print("\nInclude override detected. Using the provided include rules.\n")
            include_rules = state['include_override']
        else:
            include_rules = self._load_pattern(os.path.join(project_path, ".k/includes.txt")) or ""
        
        exclude_rules = self._load_pattern(os.path.join(project_path, ".k/excludes.txt")) or ""

        print(f"\nInclude rules: {include_rules}")
        print(f"Exclude rules: {exclude_rules}\n")

        return {"include_rules": include_rules, "exclude_rules": exclude_rules, "progress": "Include and exclude rules loaded."}
    
    def _load_pattern(self, file_path: str) -> Optional[str]:
        """
        Helper method to load and concatenate pattern lines from a file.

        Reads the given file, strips empty lines, and concatenates them with '|'
        which can be used as a regex pattern for matching.
        Returns:
            The concatenated pattern string, or None if the file does not exist.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                rules = [line.strip() for line in lines if line.strip()]
                return "|".join(rules) if rules else None
        except FileNotFoundError:
            return None
