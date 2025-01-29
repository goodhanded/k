from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from application.agency.dtos import ToolResponseDTO

class ToolInterface(Protocol):
  def invoke(self, prompt: str) -> 'ToolResponseDTO':
    pass