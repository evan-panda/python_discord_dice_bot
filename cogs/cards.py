from discord.ext import commands
from discord import Interaction, app_commands
from random import randint


class Cards(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cards cog loaded.')

    @app_commands.command(name='draw', description='Draws a random card.')
    async def draw(self, interaction: Interaction):
        suit_n = randint(0, 3)
        num = randint(1, 13)

        suits = {0: "Spades", 1: "Diamonds", 2: "Clubs", 3: "Hearts"}
        f_card = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

        # get face card name if num is 1 or > 10, otherwise, use num
        card = num if 2 < num < 11 else f_card.get(num)

        await interaction.response.send_message(f"You drew the {card} of {suits.get(suit_n)}")


async def setup(bot):
    await bot.add_cog(Cards(bot))
