import asyncio
from typing import Callable

import discord
import neispy

from utils import is_mobile


class Utils:
    def __init__(self, Bot):
        self.Bot = Bot

    async def pagination(self, ctx, callback: Callable, limit: int):
        position = 0

        message = await ctx.send(embed=callback(position), mobile=is_mobile(ctx.author))

        async def _add_emojis():
            try:
                for emoji in ["◀", "⏹", "▶"]:
                    await message.add_reaction(emoji)
            except:
                pass

        self.Bot.loop.create_task(_add_emojis())

        while not self.Bot.is_closed():
            try:
                reaction, user = await self.Bot.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: user == ctx.author
                    and reaction.message.id == message.id
                    and reaction.emoji in ["◀", "⏹", "▶"],
                    timeout=30,
                )
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

            if reaction.emoji == "◀" and position > 0:
                position -= 1
            elif reaction.emoji == "⏹":
                try:
                    await message.clear_reactions()
                except:
                    pass
                break
            elif reaction.emoji == "▶" and position < limit:
                position += 1

            await message.edit(embed=callback(position), mobile=is_mobile(ctx.author))
            await message.remove_reaction(reaction.emoji, user)

    async def search_school(self, ctx, query: str) -> dict:
        try:
            Data = await self.Bot.neis.schoolInfo(SCHUL_NM=query)
        except neispy.DataNotFound:
            await ctx.send(
                embed=discord.Embed(
                    title="학교 정보가 없습니다. 확인 후 다시 시도해주세요.", colur=discord.Colour.red()
                )
            )
            return

        school_list = [
            f"{index}. {school.SCHUL_NM} ({school.LCTN_SC_NM})"
            for index, school in enumerate(Data, 1)
        ]

        return await self.select_list(ctx, Data, school_list)

    async def select_list(
        self, ctx, Data: list, string_list: list = None, title: str = "여러개의 검색 결과입니다."
    ):
        if not string_list:
            string_list = [f"{index}. {Value}" for index, Value in enumerate(Data, 1)]

        if not isinstance(Data, list):
            Data = list(Data)

        if len(Data) == 1:
            return Data[0]
        Data = Data[:10]

        message = await ctx.send(
            embed=discord.Embed(
                title=title,
                description="\n".join(string_list),
                colur=discord.Colour.blurple(),
            ),
            mobile=is_mobile(ctx.author),
        )

        try:
            response = await self.Bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == message.channel,
                timeout=30.0,
            )
        except asyncio.TimeoutError:
            await message.edit(
                embed=discord.Embed(
                    title="시간 초과 입니다. 처음부터 다시 시도 해주세요.",
                    colur=discord.Colour.red(),
                    mobile=is_mobile(ctx.author),
                )
            )
            return

        if not response.content.isdigit() or 1 > int(response.content) > len(Data):
            await message.edit(
                embed=discord.Embed(
                    title="잘못된 값을 받았습니다. 확인 후 다시 시도 해주세요.",
                    colur=discord.Colour.red(),
                    mobile=is_mobile(ctx.author),
                )
            )
            return

        await message.delete()

        return Data[int(response.content) - 1]


def setup(Bot):
    utils = Utils(Bot)

    Bot.pagination = utils.pagination
    Bot.search_school = utils.search_school
    Bot.select_list = utils.select_list
