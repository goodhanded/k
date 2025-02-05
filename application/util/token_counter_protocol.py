from typing import Protocol

class TokenCounterProtocol(Protocol):
    def count_tokens(self, text: str) -> int:
        ...
