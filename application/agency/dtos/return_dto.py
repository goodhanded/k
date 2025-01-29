from dataclasses import dataclass
from application.dto import DataTransferObject
from typing import Optional

@dataclass
class ReturnDefinition(DataTransferObject):
    type: str
    description: str
    items: Optional[list[DataTransferObject]]
