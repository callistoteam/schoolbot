import inspect
from typing import Callable
import discord
import asyncio
import neispy


async def pagination(self, ctx, callback: Callable, limit: int):
    position = 0

    message = await ctx.send(embed=callback(position))

    async def _add_emojis():
        try:
            for emoji in ["◀", "⏹", "▶"]:
                await message.add_reaction(emoji)
        except:
            pass

    self.loop.create_task(_add_emojis())

    while not self.is_closed():
        try:
            reaction, user = await self.wait_for(
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

        await message.edit(embed=callback(position))
        await message.remove_reaction(reaction.emoji, user)


async def search_school(self, ctx, query: str) -> dict:
    try:
        Data = await self.neis.schoolInfo(SCHUL_NM=query)
    except neispy.DataNotFound:
        await ctx.send(
            embed=discord.Embed(
                title="학교 정보가 없습니다. 확인 후 다시 시도해주세요.", colur=discord.Colour.red()
            )
        )
        return

    if len(Data) == 1:
        return Data[0]

    school_list = [
        f"{index}. {school.SCHUL_NM} ({school.LCTN_SC_NM})"
        for index, school in enumerate(Data, 1)
    ]

    message = await ctx.send(
        embed=discord.Embed(
            title="여러개의 검색 결과입니다.",
            description="\n".join(school_list),
            colur=discord.Colour.blurple(),
        )
    )

    try:
        response = await self.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.channel == message.channel,
            timeout=30.0,
        )
    except asyncio.TimeoutError:
        await message.edit(
            embed=discord.Embed(
                title="시간 초과 입니다. 처음부터 다시 시도 해주세요.", colur=discord.Colour.red()
            )
        )
        return

    await message.delete()

    if not response.content.isdigit():
        await message.edit(
            embed=discord.Embed(
                title="잘못된 값을 받았습니다. 확인 후 다시 시도 해주세요.", colur=discord.Colour.red()
            )
        )
        return

    return Data[int(response.content) - 1]


def setup(Bot):
    Bot.pagination = pagination
    Bot.search_school = search_school