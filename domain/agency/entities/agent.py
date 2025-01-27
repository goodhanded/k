from typing import List
from .agent_tool import AgentTool
from domain.util.yaml import load_yaml
from domain.util.module_resolution import resolve_module

TOOLS_YAML_PATH = 'domain/agency/tools.yaml'
AGENTS_YAML_PATH = 'domain/agency/agents.yaml'

class Agent:
    def __init__(self, name: str):
        self.tools: List[AgentTool] = []
        self.load_tool_definitions()
        self.load(name)

    def load_tool_definitions(self):
        self.tool_definitions = load_yaml(TOOLS_YAML_PATH, "tools")

    def load(self, name: str):
        agents = load_yaml(AGENTS_YAML_PATH, "agents")
        agent_def = next((agent for agent in agents if agent['name'] == name), None)
        if agent_def is None:
            raise Exception(f'Agent {name} not found in agents.yaml')
        self.name = agent_def['name']
        self.model = agent_def['model']
        self.role = agent_def['role']

        for tool_name in agent_def['tools']:
            self.add_tool(tool_name)

    def add_tool(self, tool_name: str):
        tool_def = next((tool for tool in self.tool_definitions if tool['name'] == tool_name), None)

        if tool_def is None:
            raise Exception(f'Tool {tool_name} not found in tools.yaml')
        
        self.tools.append(AgentTool(tool_def))

    def prompt(self, prompt: str):
        # Test output
        print(f'{self.name} is prompted with: {prompt}')
        print(f'{self.name} has the following tools: {self.tools}')
