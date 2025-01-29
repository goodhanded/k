from typing import Optional
from dataclasses import dataclass
from application.dto import DataTransferObject
from .method_dto import MethodDTO

@dataclass
class ToolResponseDTO(DataTransferObject):
    errors: Optional[list[str]]
    result: str