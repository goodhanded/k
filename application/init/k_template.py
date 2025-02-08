from typing import Protocol

class KTemplateProtocol(Protocol):
    def get_excludes(self) -> str:
        """Return the content for the .k/excludes.txt file."""
        ...

    def get_includes(self) -> str:
        """Return the content for the .k/includes.txt file."""
        ...

    def get_rules(self) -> str:
        """Return the content for the .k/rules.txt file."""
        ...
