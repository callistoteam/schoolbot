import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx):
        embed = discord.Embed(title="도움말", description="접두사: ``?``")

        for Command in [i for i in self.Bot.commands if i.help]:
            embed.add_field(
                name=Command.name,
                value=Command.help,
                inline=False,
            ).add_field(
                name="유용한 링크",
                value="[이용약관](https://callisto.team/tos)\n[개인정보취급방침](https://callisto.team/privacy),
                inline=False,
            )

        await ctx.send(embed=embed)


def setup(Bot):
    Bot.add_cog(Help(Bot))
