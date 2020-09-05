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
            )

        await ctx.send(embed=embed)


def setup(Bot):
    Bot.add_cog(Help(Bot))
