from typing import Protocol

class LLMClientProtocol(Protocol):

    model: str

    def chat(self, model: str, prompt: str) -> str:
        pass
