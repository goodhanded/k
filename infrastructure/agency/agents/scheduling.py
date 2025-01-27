from application.agency import AgentInterface

class SchedulingAgent(AgentInterface):
    def invoke(self, prompt: str):
        return "scheduling agent invoked"