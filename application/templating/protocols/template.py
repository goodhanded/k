from typing import Protocol

class TemplateProtocol(Protocol):
    def format(self, **kwargs) -> str:
        pass