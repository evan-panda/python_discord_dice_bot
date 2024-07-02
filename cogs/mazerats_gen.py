# system
import os

# imports
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Interaction, app_commands

# personal
from generators.maze_rats_generators.src.main_gen import main

load_dotenv()
test_server_id = os.environ['test_server_id']


class MazeRats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """
    Select generator:
    [1] Spell Name - by the book
    [2] Spell Name - random
    [3] Character Details
    [4] Character Items
    """

    @app_commands.command(
        name='ratgen',
        description='Generate a random item for Maze Rats',
    )
    @app_commands.describe(generator='Select item to generate')
    @app_commands.choices(generator=[
        app_commands.Choice(name='character details', value='3'),
        app_commands.Choice(name='character items', value='4'),
        app_commands.Choice(name='spell name', value='1'),
        # app_commands.Choice(name='spell name (random)', value='2'),
    ])
    async def rat_gen(
        self,
        interaction: Interaction,
        generator: discord.app_commands.Choice[str],
        whisper: bool = False
    ) -> None:
        """
        Generate random item for Maze Rats
        - Command: /ratgen
        """
        ephemeral_flag = whisper

        description = main(generator=generator.value)

        message = f"Generated: {generator.name}\n---\n" + description

        await interaction.response.send_message(message, ephemeral=ephemeral_flag)


async def setup(bot) -> None:
    await bot.add_cog(MazeRats(bot))
