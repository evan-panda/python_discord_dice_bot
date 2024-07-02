# system
import os

# imports
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Interaction, app_commands

# personal
from generators.bitd_gen.src.doskvolMasterGenerator import main


load_dotenv()
test_server_id = os.environ['test_server_id']


class BitD(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """
    Select generator:
[1]  Create common NPC
[2]  Create rare NPC
[3]  Create street description
[4]  Create common building description
[5]  Create rare building description
[6]  Create a demon
[7]  Create a ghost
[8]  Create a cult
[9]  Create a score
[10] Create a leviathan doing banal activity
[11] Create a leviathan doing surreal activity
[12] Create a leviathan spawn
    """

    @app_commands.command(
        name='bdgen',
        description='Generate a random item for Blades in the Dark',
    )
    @app_commands.describe(generator='Select item to generate')
    @app_commands.choices(generator=[
        app_commands.Choice(name='npc common', value='1'),
        app_commands.Choice(name='npc rare', value='2'),
        app_commands.Choice(name='street description', value='3'),
        app_commands.Choice(name='building common', value='4'),
        app_commands.Choice(name='building rare', value='5'),
        app_commands.Choice(name='demon', value='6'),
        app_commands.Choice(name='ghost', value='7'),
        app_commands.Choice(name='cult', value='8'),
        app_commands.Choice(name='score', value='9'),
        app_commands.Choice(name='leviathan banal activity', value='10'),
        app_commands.Choice(name='leviathan surreal activity', value='11'),
        app_commands.Choice(name='leviathan spawn', value='12')
    ])
    async def bitd_gen(
        self,
        interaction: Interaction,
        generator: discord.app_commands.Choice[str],
        whisper: bool = True
    ) -> None:
        """
        Generate random item for Blades in the Dark
        - Command: /bdgen
        """
        ephemeral_flag = whisper

        description = main(generator=generator.value)

        message = f"Generated: {generator.name}\n" + description

        await interaction.response.send_message(message, ephemeral=ephemeral_flag)


async def setup(bot):
    await bot.add_cog(BitD(bot))
