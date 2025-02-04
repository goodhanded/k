from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.registry import Registry

class PromptAgentUseCase:
    def __init__(self, agent_registry: 'Registry'):
        self.agent_registry = agent_registry

    def execute(self, agent_name: str, prompt: str):
        agent = self.agent_registry.get(agent_name)

        if agent is None:
            return

        print(f'Invoking agent: {agent_name}')
        response = agent.invoke(prompt)

        return response
