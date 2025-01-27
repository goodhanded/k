from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_registry import AgentInterface

class AgentRegistryInterface(Protocol):
  def get(agent_name: str) -> 'AgentInterface':
    pass