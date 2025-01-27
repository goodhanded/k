from dataclasses import dataclass

@dataclass
class AgentResponse:
    prompt: str
    response: str
    agent: str
    session: str
    timestamp: str
    status: str
    error: str
    def __str__(self):
        return f'{self.response}'