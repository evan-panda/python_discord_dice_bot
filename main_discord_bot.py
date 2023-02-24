#!./venv/bin/python
import discord
from discord import app_commands, Intents, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.environ['discord_bot_token']
test_server_id = os.environ['test_server_id']


class BotClient(commands.Bot):
    def __init__(self, *, command_prefix: str = ".", intents: Intents = discord.Intents.default(), **options) -> None:
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents, **options)

    async def on_ready(self):
        await self.wait_until_ready()
        await self.__load_cogs()

        print('all cogs loaded.')
        print(f'Logged in as {self.user}')

    # @commands.command(name='test')
    @app_commands.command(name='test', description='testing commands')
    async def test(self, interaction: Interaction) -> None:
        print('hi from test cmd')
        # await ctx.send('hello there!')
        await interaction.response.send_message("hello there!")

    async def __load_cogs(self):
        print('getting cog file list:')
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                print(f'loading - cogs.{file[:-3]}')
                await self.load_extension(f'cogs.{file[:-3]}')


def main():
    # initialize bot client
    print('initialize bot')
    bot = BotClient()

    print('running bot')
    bot.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
