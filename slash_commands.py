# working on desktop pc
import os
from dotenv import load_dotenv

import discord
from discord import Intents, Interaction
from discord import app_commands

from dice_roller import handle_rolls
from random import randint

load_dotenv()
bot_token = os.environ['discord_bot_token']
test_server_id = os.environ['test_server_id']


class aclient(discord.Client):

    def __init__(self, *, intents: Intents = Intents.default(),
                 **options) -> None:
        super().__init__(intents=intents, **options)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=test_server_id))

        print(f'Logged in as {self.user}')


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name='test',
              description='testing',
              guild=discord.Object(id=test_server_id))
async def self(interaction: Interaction, name: str):
    print('/test - command executed')
    await interaction.response.send_message(
        f'Hello {name}! I was made with Discord.py!', ephemeral=True)


@tree.command(name='20',
              description='Roll 1d20',
              guild=discord.Object(id=test_server_id))
async def roll20(interaction: Interaction):
    roll = str(randint(1, 20))
    print(f"'/20' - command executed - result: {roll}")
    await interaction.response.send_message(roll)


@tree.command(name='r',
              description='Rolls dice from given formula. e.g. "1d20+2"',
              guild=discord.Object(id=test_server_id))
async def roll(interaction: Interaction, rolls: str, type: str = "s"):
    print(f'user input rolls: {rolls}\ntype: {type}')
    roll_output = handle_rolls(rolls)
    if len(roll_output) > 1 and isinstance(roll_output, list):
        roll_output = '\n'.join(roll_output)
    await interaction.response.send_message(roll_output)


def run_bot():
    client.run(bot_token)

if __name__ == '__main__':
    run_bot()

