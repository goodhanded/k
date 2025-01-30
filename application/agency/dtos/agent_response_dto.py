from typing import List
from dataclasses import dataclass, field
from application.dto import DataTransferObject

@dataclass
class AgentResponseDTO(DataTransferObject):
    prompt: str
    response: str
    agent: str
    timestamp: str
    success: bool
    errors: List[str] = field(default_factory=list)
    def __str__(self):
        return f'{self.response}'