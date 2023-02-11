import discord
from discord import app_commands, Intents, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv
# from typing import Optional, Literal


load_dotenv()
bot_token = os.environ['discord_bot_token']
test_server_id = os.environ['test_server_id']


class BotClient(commands.Bot):
    def __init__(self, *, command_prefix: str = ".", intents: Intents = discord.Intents.default(), **options) -> None:
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        self.synced = False

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

    # # add sync command
    # @bot.command()
    # @commands.guild_only()
    # @commands.is_owner()
    # async def sync(
    #     ctx: commands.Context,
    #     guilds: commands.Greedy[discord.Object],
    #     spec: Optional[Literal["~", "*", "^"]] = None
    # ) -> None:
    #     """
    #     Works like:
    #     - `.sync` -> global sync
    #     - `.sync ~` -> sync current guild
    #     - `.sync *` -> copies all global app commands to current guild and syncs
    #     - `.sync ^` -> clears all commands from the current guild target and syncs (removes guild commands)
    #     - `.sync id_1 id_2` -> syncs guilds with id 1 and 2
    #     """
    #     if not guilds:
    #         if spec == "~":
    #             synced = await ctx.bot.tree.sync(guild=ctx.guild)
    #         elif spec == "*":
    #             ctx.bot.tree.copy_global_to(guild=ctx.guild)
    #             synced = await ctx.bot.tree.sync(guild=ctx.guild)
    #         elif spec == "^":
    #             ctx.bot.tree.clear_commands(guild=ctx.guild)
    #             await ctx.bot.tree.sync(guild=ctx.guild)
    #             synced = []
    #         else:
    #             synced = await ctx.bot.tree.sync()
    #         await ctx.send(
    #             f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
    #         )
    #         return
    #     ret = 0
    #     for guild in guilds:
    #         try:
    #             await ctx.bot.tree.sync(guild=guild)
    #         except discord.HTTPException:
    #             pass
    #         else:
    #             ret += 1
    #     await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    print('running bot')
    bot.run(bot_token)


if __name__ == '__main__':
    main()

