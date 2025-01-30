from typing import TYPE_CHECKING
from infrastructure.discord import DiscordBot

if TYPE_CHECKING:
    from application.agency import AgentFactoryProtocol, PromptAgentUseCase

class RunDiscordBotUseCase:

    def __init__(self, prompt_agent_use_case: 'PromptAgentUseCase'):
        self.prompt_agent_use_case = prompt_agent_use_case

    def execute(self):
        bot = DiscordBot(self.prompt_agent_use_case)
        bot.run()