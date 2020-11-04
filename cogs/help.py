import discord
from discord.ext import commands

from utils import is_mobile


class Help(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx):
        embed = discord.Embed(
            title="도움말", description=f"접두사: ``{self.Bot.command_prefix}``"
        )

        for Command in [
            i for i in self.Bot.commands if i.help if "jishaku" not in i.name
        ]:
            embed.add_field(
                name=Command.name,
                value=Command.help,
                inline=False,
            )
        embed.add_field(
            name="유용한 링크",
            value="[이용약관](https://callisto.team/tos)\n[개인정보취급방침](https://callisto.team/privacy)",
            inline=False,
        )
        await ctx.send(embed=embed, mobile=is_mobile(ctx.author))


def setup(Bot):
    Bot.add_cog(Help(Bot))
