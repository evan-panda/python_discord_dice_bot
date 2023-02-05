import os
from dotenv import load_dotenv

import discord
from discord import Intents, Interaction
from discord import app_commands

from dice_roller import DiceRoller
from dice_roller import help_message
from random import randint

load_dotenv()
bot_token = os.environ['discord_bot_token']
test_server_id = os.environ['test_server_id']


class DClient(discord.Client):
    def __init__(self, *, intents: Intents = Intents.default(), **options) -> None:
        super().__init__(intents=intents, **options)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            cmd_list = await tree.sync(guild=discord.Object(id=test_server_id))  # noqa: F841
            print('command list synced')
            # print(cmd_list)

        print(f'Logged in as {self.user}')


client = DClient()
tree = app_commands.CommandTree(client)


@tree.command(
    name='ping',
    description='ping time',
    guild=discord.Object(id=test_server_id)
)
async def ping(interaction: Interaction):
    """See how long the bot takes to respond"""
    await interaction.response.send_message(f'Pong! {round(client.latency * 1000)}ms', ephemeral=True)


@tree.command(
    name='hello',
    description='Enter your name and say hi!',
    guild=discord.Object(id=test_server_id)
)
async def hello(interaction: Interaction, name: str):
    """Say hi to user"""
    print(f"'/hello' - command executed - with {name}")
    await interaction.response.send_message(
        f'Hello {name}! I was made with Discord.py!', ephemeral=True)


@tree.command(
    name='help',
    description='Prints a useful message with example roll input and what the supported roll types are.',
    guild=discord.Object(id=test_server_id)
)
async def help(interaction: Interaction):
    """Print help message to user"""
    await interaction.response.send_message(help_message, ephemeral=True)


@tree.command(
    name='20',
    description='Roll 1d20',
    guild=discord.Object(id=test_server_id)
)
async def roll20(interaction: Interaction):
    """Roll 1d20"""
    roll = str(randint(1, 20))
    print(f"'/20' - command executed - result: {roll}")
    await interaction.response.send_message(f'Rolling: 1d20\nRolled: ({roll})')


@tree.command(
    name='r',
    description='Rolls dice from user input. e.g. 1d20+2',
    guild=discord.Object(id=test_server_id)
)
@app_commands.describe(rolls='Format: 2d6, 1d20+2+1d4')
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
async def roll(interaction: Interaction, rolls: str, roll_type: discord.app_commands.Choice[str]):
    """Roll dice formula input by user"""
    print(f"'/r' - command executed - user input rolls: {rolls}\ntype: {roll_type.value}")
    ephemeral_flag = False
    roller = DiceRoller()

    roll_output = roller.handle_rolls(rolls, roll_type.value)

    # check if the returned value is a list, or the start of the help message
    if len(roll_output) > 1 and isinstance(roll_output, list):
        message = '\n'.join(roll_output)
    elif roll_output.strip().startswith('Input Examples'):
        # make it so only the person sending the help message can see it
        ephemeral_flag = True
        message = roll_output

    if len(roll_output) < 2000:
        await interaction.response.send_message(message, ephemeral=ephemeral_flag)
    else:
        message = '\n'.join([
            roll_output[0],
            roll_output[1],
            roll_output[3],
            "The message is too large, please roll less dice if you would like to see the individual results."
        ])
        await interaction.response.send_message(message)


def run_bot():
    client.run(bot_token)


if __name__ == '__main__':
    run_bot()
