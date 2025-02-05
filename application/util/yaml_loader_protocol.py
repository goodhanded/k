from typing import Any, Optional, Protocol

class YamlLoaderProtocol(Protocol):
    def load_yaml(self, file_path: str, subpath: Optional[Any] = None) -> Any:
        ...
