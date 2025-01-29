from dataclasses import dataclass
from application.dto import DataTransferObject
from .method_dto import MethodDTO

@dataclass
class ToolDTO(DataTransferObject):
    name: str
    description: str
    methods: list[MethodDTO]