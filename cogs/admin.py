import discord
from discord.ext import commands
from discord import Interaction, app_commands
from typing import Optional, Literal
from dotenv import load_dotenv
import os


load_dotenv()
test_server_id = os.environ['test_server_id']


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.help_msg = (
            "sync options:\n"
            ".sync = global\n"
            ".sync ~ = current guild\n"
            ".sync * = copies global to current guild and syncs\n"
            ".sync ^ = clears commands from current guild and syncs\n"
            ".sync id_1 id_2 = syncs guilds with id 1 and 2"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        """Print message when cog loaded and ready"""
        print('Admin cog loaded.')

    @app_commands.command(
        name='hello',
        description='Enter your name and say hi!'
    )
    async def hello(self, interaction: Interaction, name: str = ""):
        """Say hi to user"""
        print(f"'/hello' - command executed - with {name}")
        await interaction.response.send_message(
            f'Hello {name if name else interaction.user}! I am a bot that was made with Discord.py!', ephemeral=True
        )

    @app_commands.command(
        name='ping',
        description='Prints latency.'
    )
    @commands.has_permissions(administrator=True)
    async def ping(self, interaction: Interaction):
        """See how long the bot takes to respond"""
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms', ephemeral=True)

    @commands.command(name='sync-help')
    async def sync_help(self, ctx: commands.Context) -> None:
        await ctx.send(self.help_msg)

    # add sync command
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None
    ) -> None:
        """
        Works like:
        - `.sync` -> global sync
        - `.sync ~` -> sync current guild
        - `.sync *` -> copies all global app commands to current guild and syncs
        - `.sync ^` -> clears all commands from the current guild target and syncs (removes guild commands)
        - `.sync id_1 id_2` -> syncs guilds with id 1 and 2
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(Admin(bot), guilds=[discord.Object(id=test_server_id)])
