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

    def __init__(self, *, intents: Intents = Intents.default(),
                 **options) -> None:
        super().__init__(intents=intents, **options)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            cmd_list = await tree.sync(guild=discord.Object(id=test_server_id))
            print('command list synced')
            print(cmd_list)

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
async def self(interaction: Interaction, name: str):
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
async def roll(interaction: Interaction, rolls: str, type: str = "s"):
    """Roll dice formula input by user"""
    print(f"'/r' - command executed - user input rolls: {rolls}\ntype: {type}")
    ephemeral_flag = False
    roller = DiceRoller()

    roll_output = roller.handle_rolls(rolls, type)

    # check if the returned value is a list, or the start of the help message
    if len(roll_output) > 1 and isinstance(roll_output, list):
        roll_output = '\n'.join(roll_output)
    elif roll_output.strip().startswith('Input Examples'):
        # make it so only the person sending the help message can see it
        ephemeral_flag = True

    if len(roll_output) < 2000:
        await interaction.response.send_message(roll_output, ephemeral=ephemeral_flag)
    else:
        await interaction.response.send_message("The message is too large, please roll less dice.")


def run_bot():
    client.run(bot_token)


if __name__ == '__main__':
    run_bot()
