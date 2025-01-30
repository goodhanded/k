import discord
from discord.ext import commands
from infrastructure.config import ConfigService
from application.agency import PromptAgentUseCase


class DiscordBot:
    def __init__(self, prompt_agent_use_case: PromptAgentUseCase):
        self.config = ConfigService()
        self.token = self.config.require('DISCORD_BOT_TOKEN')

        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            print(f"Bot is online! Logged in as {self.bot.user}")

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            response = prompt_agent_use_case.execute(str(message.channel), message.content)
            await message.channel.send(response)
            
            
    def run(self):
        self.bot.run(self.token)

if __name__ == "__main__":
    bot_instance = DiscordBot()
    bot_instance.run()
