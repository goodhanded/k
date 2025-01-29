from domain.util.yaml import load_yaml
from application.agency import AgentDTO, AgentFactoryInterface, AgentInterface, ToolFactoryInterface
from .agent import Agent

AGENT_YAML_PATH = 'agents.yaml'

class AgentFactory(AgentFactoryInterface):

    def __init__(self, tool_factory: ToolFactoryInterface):
        self.tool_factory = tool_factory

    def create(self, agent_name: str) -> AgentInterface:
        """
        Method that returns an 'AgentInterface' instance.
        """
        agent_yaml_key = ["agents", agent_name]

        try:
            agent_definition = AgentDTO.from_yaml(AGENT_YAML_PATH, agent_yaml_key)
        except ValueError as e:
            return None

        agent = Agent(agent_definition)
        
        if agent_definition.tools and len(agent_definition.tools) > 0:
            tools = self.tool_factory.create_all(agent_definition.tools)
            agent.add_tools(tools)

        return agent