from typing import Protocol
from ..dtos import AgentResponseDTO

class AgentProtocol(Protocol):
  def invoke(self, prompt: str) -> AgentResponseDTO:
    pass
