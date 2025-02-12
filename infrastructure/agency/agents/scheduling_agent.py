from application.agency import WorkflowProtocol

class SchedulingAgent(WorkflowProtocol):
    def __init__(self):
        self.name = 'Scheduling Agent'
        self.model = 'Simple Scheduling Model'
        self.description = 'This agent schedules appointments based on user input.'
        
    def run(self, prompt: str):
        # Test output
        print(f'{self.name} is prompted with: {prompt}')
        return None

    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'