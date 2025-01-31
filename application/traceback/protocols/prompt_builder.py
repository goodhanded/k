from typing import Protocol

class PromptBuilderProtocol(Protocol):
    def build(self) -> str:
        pass