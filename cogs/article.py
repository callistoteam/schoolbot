import asyncio
from datetime import datetime

import discord
import iamschool
from discord.ext import commands
from iamschool import HTTPException

from database import User


class Article(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot
        self.client = iamschool.AsyncClient()

    @commands.command(name="게시물")
    async def _article(self, ctx, schoolname: str = None):
        """
        설명:해당학교의 아이엠스쿨 게시물을 가져옵니다.
        인자값: 학교명(필수)
        예시:
        ?게시물 인천기계공업고등학교
        """

        if schoolname:
            try:
                Data = await self.client.search_school(schoolname)
            except HTTPException:
                return await ctx.send(
                    embed=discord.Embed(
                        title="HTTP 요청 오류입니다",
                        colour=discord.Colour.red(),
                    )
                )

            if not Data:
                return await ctx.send(
                    embed=discord.Embed(
                        title="아이엠스쿨에 등록되지 않았습니다. 확인하신후 다시 요청하세요",
                        description=" [아이엠스쿨 바로가기](https://school.iamservice.net/) ",
                        colour=discord.Colour.red(),
                    )
                )

            if len(Data) == 1:
                Data = Data[0]
            else:
                school_list = [
                    f"{index}. {school.name}" for index, school in enumerate(Data, 1)
                ]

                message = await ctx.send(
                    embed=discord.Embed(
                        title="여러개의 검색 결과입니다.",
                        description="\n".join(school_list),
                        colur=discord.Colour.blurple(),
                    )
                )

                try:
                    response = await self.Bot.wait_for(
                        "message",
                        check=lambda m: m.author == ctx.author
                        and m.channel == message.channel,
                        timeout=30.0,
                    )
                except asyncio.TimeoutError:
                    return await message.edit(
                        embed=discord.Embed(
                            title="시간 초과 입니다. 처음부터 다시 시도 해주세요.",
                            colur=discord.Colour.red(),
                        )
                    )

                await message.delete()

                if not response.content.isdigit():
                    return await message.edit(
                        embed=discord.Embed(
                            title="잘못된 값을 받았습니다. 확인 후 다시 시도 해주세요.",
                            colur=discord.Colour.red(),
                        )
                    )

                Data = Data[int(response.content) - 1]
            school_id = Data.id
        else:
            Data = await User.get_or_none(id=ctx.author.id)
            if not Data:
                return await ctx.send(
                    embed=discord.Embed(
                        title="학교명을 입력 해주시기 바랍니다.", colur=discord.Colour.red()
                    )
                )

            school_id = Data.iamschool

        try:
            articles = await self.client.fetch_recent_article(school_id)
        except HTTPException:
            return await ctx.send(
                embed=discord.Embed(
                    title="HTTP 요청 오류입니다",
                    colour=discord.Colour.red(),
                )
            )

        if not articles:
            return await ctx.send(
                embed=discord.Embed(
                    title="아이엠스쿨에 게시된 게시물이 없습니다.",
                    description=" [아이엠스쿨 바로가기](https://school.iamservice.net/)",
                    colour=discord.Colour.red(),
                )
            )

        def callback(position):
            embed = (
                discord.Embed(
                    title=articles[position].title,
                    description=articles[position].content,
                    timestamp=datetime.strptime(articles[position].date, "%Y.%m.%d"),
                    url=articles[position].link,
                    colour=0x2E3136,
                )
                .set_author(
                    name=articles[position].organization_name,
                    url=f"https://school.iamservice.net/organization/{articles[position].organization_id}",
                    icon_url=articles[position].organization_logo,
                )
                .set_footer(
                    text=f"#{articles[position].group.name} • {articles[position].author}"
                )
            )
            if articles[position].images:
                embed.set_image(url=articles[position].images[0])

            return embed

        await self.Bot.pagination(ctx, callback, limit=len(articles))


def setup(Bot):
    Bot.add_cog(Article(Bot))
