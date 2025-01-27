from typing import Protocol
from domain.agency import AgentResponse

class AgentInterface(Protocol):
  def invoke(self, prompt: str) -> AgentResponse:
    pass