from .bot import load_cogs
from discord.ext.commands import Bot as Core

bot = Core(command_prefix="*", help_command=None)
load_cogs(bot)
bot.run(token)