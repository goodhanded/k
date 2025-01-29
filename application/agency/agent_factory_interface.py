from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from .agent_factory_interface import AgentInterface

class AgentFactoryInterface(Protocol):
  def create(agent_name: str) -> 'AgentInterface':
    pass