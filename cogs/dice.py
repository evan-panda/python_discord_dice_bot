# system
import os
from random import randint

# imports
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Interaction, app_commands

# personal
import dice_handler


load_dotenv()
test_server_id = os.environ['test_server_id']


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Dice cog loaded.')

    @app_commands.command(name='dice-help', description='See help message for dice.')
    async def dice_help(self, interaction: Interaction):
        """
        Prints help message
        """
        await interaction.response.send_message(dice_handler.help_message, ephemeral=True)

    @app_commands.command(name='20', description='Roll 1d20')
    async def roll20(self, interaction: Interaction):
        """
        Rolls 1d20
        - Command: /20
        """
        roll = str(randint(1, 20))
        print(f"'/20' - command executed - result: {roll}")
        await interaction.response.send_message(f'Rolling: 1d20\nRolled: ({roll})')

    @app_commands.command(
        name='r',
        description='Rolls dice from user input. e.g. 1d20+2',
    )
    @app_commands.describe(rolls='Format examples: 2d6, 1d20+2+1d4')
    @app_commands.describe(roll_type='Select')
    @app_commands.choices(roll_type=[
        discord.app_commands.Choice(name='Standard', value='s'),
        discord.app_commands.Choice(name='Advantage', value='a'),
        discord.app_commands.Choice(name='Disadvantage', value='d'),
        discord.app_commands.Choice(name='Best', value='b'),
        discord.app_commands.Choice(name='Worst', value='w'),
        discord.app_commands.Choice(name='Pool', value='p'),
        discord.app_commands.Choice(name='Drop Lowest', value='l'),
        discord.app_commands.Choice(name='Drop Highest', value='h')
    ])
    async def roll(self, interaction: Interaction, rolls: str, roll_type: discord.app_commands.Choice[str]):
        """
        Roll dice formula input by user
        - Command: /r
        """
        print(f"'/r' - command executed - user input rolls: {rolls}\ntype: {roll_type.value}")
        ephemeral_flag = False
        roller = dice_handler.DiceRoller(debug=True)

        roll_output = roller.handle_rolls(rolls, roll_type.value)

        # check if the returned value is a list, or the start of the help message
        if len(roll_output) > 1 and isinstance(roll_output, list):
            message = '\n'.join(roll_output)
        elif roll_output.strip().startswith('Input Examples'):
            # make it so only the person sending the help message can see it
            ephemeral_flag = True
            message = roll_output
        else:
            message = roll_output

        if len(message) < 2000:
            await interaction.response.send_message(message, ephemeral=ephemeral_flag)
        elif isinstance(roll_output, list):
            message = '\n'.join([
                roll_output[0],
                roll_output[1],
                roll_output[3],
                "The message is too large, please roll less dice if you would like to see the individual results."
            ])
            await interaction.response.send_message(message, ephemeral=ephemeral_flag)
        else:
            await interaction.response.send_message(
                "Something unexpected has occured. Please double check your input and try again.",
                ephemeral=ephemeral_flag
            )


async def setup(bot):
    await bot.add_cog(Dice(bot), guilds=[discord.Object(id=test_server_id)])
