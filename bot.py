import os
import cogs
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cogs.load(self)


if __name__ == "__main__":
    Bot(command_prefix="?", help_command=None).run(os.environ["TOKEN"])