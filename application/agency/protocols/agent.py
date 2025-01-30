from typing import Protocol
from .tool import ToolProtocol
from ..dtos import AgentResponseDTO

class AgentProtocol(Protocol):
  def invoke(self, prompt: str) -> AgentResponseDTO:
    pass
  def add_tools(self, tools: list[ToolProtocol]) -> None:
    pass