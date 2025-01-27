from domain.agency import Agent

class TestApp:
    def __init__(self):
        self.name = 'TestApp'

    def run(self):

        agent = Agent('scheduling')
        prompt = 'What events are happening on 2021-01-01?'

        agent.prompt(prompt)
