from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import AgentRegistryInterface

class PromptAgentUseCase:
    def __init__(self, registry: 'AgentRegistryInterface'):
        self.registry = registry

    def execute(self, agent_name: str, prompt: str):
        agent = self.registry.get(agent_name)
        print(agent.invoke(prompt))