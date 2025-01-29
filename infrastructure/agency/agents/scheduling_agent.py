from application.agency import AgentInterface, ToolInterface

class SchedulingAgent(AgentInterface):
    def __init__(self):
        self.name = 'Scheduling Agent'
        self.model = 'Simple Scheduling Model'
        self.description = 'This agent schedules appointments based on user input.'
        self.tools = []
        
    def invoke(self, prompt: str):
        # Test output
        print(f'{self.name} is prompted with: {prompt}')
        print(f'{self.name} has the following tools: {self.tools}')
        return None
    def add_tools(self, tools: list[ToolInterface]):
        self.add_tool(tool for tool in tools)
    def add_tool(self, tool: ToolInterface):
        self.tools.append(tool)
    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'