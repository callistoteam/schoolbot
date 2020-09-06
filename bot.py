import logging
import os
import neispy
from discord.ext import commands

import cogs
import database

logging.basicConfig(level=logging.INFO)


class Bot(commands.Bot):
    __version__ = "1.0.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.neis = neispy.Client()  # os.environ["API_KEY"])

        cogs.load(self)
        self.load_extension("jishaku")

        self.loop.create_task(database.init())


if __name__ == "__main__":
    Bot(command_prefix="?", help_command=None).run(
        "NTAyNDczMzI1OTY1MjEzNzE4.W8iKwA.Vm0KP8BSGqyascqHjCANG842gCA"
    )  # os.environ["TOKEN"])
