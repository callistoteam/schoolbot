import discord
from discord.ext import commands

import schoolbot

from schoolbot import db


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        db.pool = await db.connect_db()

        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)

        game = discord.Game(f"?도움말 | {schoolbot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)
