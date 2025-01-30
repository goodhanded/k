from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from .tool import ToolProtocol

class ToolFactoryProtocol(Protocol):
  def create(tool_name: str) -> 'ToolProtocol':
    pass
  def create_all(tool_dtos: list[str]) -> list['ToolProtocol']:
    pass