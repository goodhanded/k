from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from .tool_interface import ToolInterface

class ToolFactoryInterface(Protocol):
  def create(tool_name: str) -> 'ToolInterface':
    pass
  def create_all(tool_dtos: list[str]) -> list['ToolInterface']:
    pass