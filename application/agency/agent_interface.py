from typing import Protocol
from .tool_interface import ToolInterface
from .dtos import AgentResponseDTO

class AgentInterface(Protocol):
  def invoke(self, prompt: str) -> AgentResponseDTO:
    pass
  def add_tools(self, tools: list[ToolInterface]) -> None:
    pass