from dataclasses import dataclass

@dataclass
class IndexResult:
    success: bool
    errors: list[str] = None
    message: str = None