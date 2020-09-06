import logging
import os

import discord
import neispy
from discord.ext import commands

import cogs
import database
import utils

logging.basicConfig(level=logging.INFO)


class Bot(commands.Bot):
    __version__ = "1.0.0"

    def __init__(self, *args, **kwargs):
        self.initialize_autoembed()

        super().__init__(*args, **kwargs)

        self.neis = neispy.Client(os.environ["API_KEY"])

        cogs.load(self)
        self.load_extension("jishaku")

        self.loop.create_task(database.init())

    def initialize_autoembed(self):
        send_method = discord.abc.Messageable.send

        async def send(self, content=None, **kwargs):
            if "embed" in kwargs and kwargs.get("mobile", True):
                if "mobile" in kwargs:
                    del kwargs["mobile"]

                if not content:
                    content = ""

                content += "\n" * 2 + utils.embed_to_text(kwargs["embed"])
                del kwargs["embed"]

            return await send_method(self, content, **kwargs)

        discord.abc.Messageable.send = send


if __name__ == "__main__":
    Bot(command_prefix="?", help_command=None).run(os.environ["TOKEN"])
