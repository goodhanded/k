import os
from typing import Optional
from application.util.project_root import find_project_root


class AddRuleUseCase:
    """
    Use case for appending a new rule to the .k/rules.txt file.
    The rule is appended as a new line in the file.
    
    This use case searches for the project root containing the .k directory.
    If not found, it instructs the user to run 'k init' first.
    """

    def __init__(self) -> None:
        pass

    def execute(self, rule: str) -> None:
        """
        Appends the given rule to the .k/rules.txt file.

        Parameters:
            rule (str): The rule text to append.
        """
        project_path = find_project_root()
        if project_path is None:
            print("Project root with a .k directory not found. Please run 'k init' first.")
            return
        
        rules_file = os.path.join(project_path, ".k", "rules.txt")
        try:
            with open(rules_file, "a", encoding="utf-8") as f:
                # Append the rule with a newline if not already present
                if not rule.endswith("\n"):
                    rule = "\n- " + rule
                f.write(rule)
            print(f"Rule added to {rules_file}: {rule.strip()}")
        except Exception as e:
            print(f"Failed to add rule: {e}")
