from dataclasses import dataclass
from application.dto import DataTransferObject

@dataclass
class AgentResponseDTO(DataTransferObject):
    prompt: str
    response: str
    agent: str
    session: str
    timestamp: str
    status: str
    error: str
    def __str__(self):
        return f'{self.response}'