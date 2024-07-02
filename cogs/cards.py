from discord.ext import commands
from discord import Interaction, app_commands
from random import choice, randint
from dotenv import load_dotenv
import os

load_dotenv()
test_server_id = os.environ['test_server_id']


class Cards(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards cog loaded.')

    @app_commands.command(name='draw-card', description='Draws a random card. (with replacement, no jokers)')
    async def draw(self, interaction: Interaction) -> None:
        num = randint(1, 13)

        suit = choice(["Spades", "Diamonds", "Clubs", "Hearts"])
        f_card = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

        # get face card name if num is 1 or > 10, otherwise, use num
        card = num if 1 < num < 11 else f_card.get(num)

        await interaction.response.send_message(f"You drew the {card} of {suit}")


async def setup(bot):
    await bot.add_cog(Cards(bot))
