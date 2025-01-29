from dataclasses import dataclass
from application.dto import DataTransferObject
from typing import Optional

@dataclass
class AgentDTO(DataTransferObject):
    name: str
    description: str
    model: str
    tools: Optional[list[str]] = None