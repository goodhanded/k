from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
  from .agent_factory import AgentInterface

class AgentFactoryProtocol(Protocol):
  def create(agent_name: str) -> 'AgentInterface':
    pass