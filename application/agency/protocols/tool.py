from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from application.agency.dtos import ToolResponseDTO

class ToolProtocol(Protocol):
  def invoke(self, prompt: str) -> 'ToolResponseDTO':
    pass