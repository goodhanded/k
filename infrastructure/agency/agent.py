from application.agency import AgentDTO, ToolInterface, AgentInterface

TOOLS_YAML_PATH = 'tools.yaml'

class Agent(AgentInterface):
    def __init__(self, agent_dto: AgentDTO):
        
        self.name = agent_dto.name
        self.model = agent_dto.model
        self.description = agent_dto.description
        self.tools = []

    def add_tool(self, tool: ToolInterface):
        self.tools.append(tool)

    def add_tools(self, tools: list[ToolInterface]):
        if tools:
            for tool in tools:
                self.add_tool(tool)

    def invoke(self, prompt: str):
        return f'{self.name} was prompted with: {prompt}'
