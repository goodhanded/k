from application.agency import AgentDTO, AgentProtocol

class Agent(AgentProtocol):
    def __init__(self, agent_dto: AgentDTO):
        
        self.name = agent_dto.name
        self.model = agent_dto.model
        self.description = agent_dto.description

    def invoke(self, prompt: str):
        return f'{self.name} was prompted with: {prompt}'
