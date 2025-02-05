import unittest

from infrastructure.agency import Agent
from application.agency import AgentDTO


class TestAgentInvocation(unittest.TestCase):
    def test_invoke(self):
        dto = AgentDTO(name="TestAgent", description="A test agent", model="TestModel")
        agent = Agent(dto)
        prompt = "Hello, world!"
        response = agent.invoke(prompt)
        self.assertIn("TestAgent was prompted with: Hello, world!", response)


if __name__ == '__main__':
    unittest.main()
