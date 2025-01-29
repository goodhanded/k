from dataclasses import dataclass
from application.dto import DataTransferObject
from .param_dto import ParamDTO

@dataclass
class MethodDTO(DataTransferObject):
    name: str
    description: str
    params: list[ParamDTO]
