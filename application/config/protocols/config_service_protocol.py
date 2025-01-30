from typing import Protocol

class ConfigServiceProtocol(Protocol):
    def get(self, key: str, default: str = None) -> str:
        pass

    def require(self, key: str) -> str:
        pass