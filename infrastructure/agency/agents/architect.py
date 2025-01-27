from application.agency import AgentInterface

class ArchitectAgent(AgentInterface):
    def invoke(self, prompt: str):
        return "architect agent invoked"