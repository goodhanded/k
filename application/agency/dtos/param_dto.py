from dataclasses import dataclass
from application.dto import DataTransferObject

@dataclass
class ParamDTO(DataTransferObject):
    name: str
    type: str
