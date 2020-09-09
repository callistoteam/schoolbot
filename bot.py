import io
import logging
import os

import aiohttp
import discord
import neispy
from discord.ext import commands

import cogs
import database
import utils

logging.basicConfig(level=logging.INFO)


class Bot(commands.Bot):
    __version__ = "1.3.0"

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
                if not content:
                    content = ""

                content += "\n" * 2 + utils.embed_to_text(kwargs["embed"])
                if kwargs["embed"].image.url != discord.Embed.Empty:
                    content += "\n" * 2 + kwargs["embed"].image.url
                del kwargs["embed"]

            if "mobile" in kwargs:
                del kwargs["mobile"]

            return await send_method(self, content, **kwargs)

        discord.abc.Messageable.send = send

        edit_method = discord.Message.edit

        async def edit(self, **kwargs):
            if "embed" in kwargs and kwargs.get("mobile", True):
                if not "content" in kwargs:
                    kwargs["content"] = ""

                kwargs["content"] += "\n" * 2 + utils.embed_to_text(kwargs["embed"])
                if kwargs["embed"].image.url != discord.Embed.Empty:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(kwargs["embed"].image.url) as resp:
                            await self.channel.send(
                                file=discord.File(
                                    io.BytesIO(await resp.content.read()),
                                    filename=f"image{os.path.splitext(kwargs['embed'].image.url)[1]}",
                                )
                            )
                del kwargs["embed"]

            if "mobile" in kwargs:
                del kwargs["mobile"]

            return await edit_method(self, **kwargs)

        discord.Message.edit = edit


if __name__ == "__main__":
    Bot(command_prefix="?", help_command=None).run(os.environ["TOKEN"])
