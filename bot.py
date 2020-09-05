import os
import cogs
from discord.ext import commands
import database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cogs.load(self)

        self.loop.create_task(database.init())


if __name__ == "__main__":
    Bot(command_prefix="?", help_command=None).run(os.environ["TOKEN"])