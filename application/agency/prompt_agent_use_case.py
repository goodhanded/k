from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.agency import AgentFactoryInterface

class PromptAgentUseCase:
    def __init__(self, agent_factory: 'AgentFactoryInterface'):
        self.agent_factory = agent_factory

    def execute(self, agent_name: str, prompt: str):
        agent = self.agent_factory.create(agent_name)

        if agent is None:
            return

        return agent.invoke(prompt)
