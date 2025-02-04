from typing import Protocol

class PromptGeneratorProtocol(Protocol):
    def generate(self, template_name: str, **template_vars) -> str:
        pass