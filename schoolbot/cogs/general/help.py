import asyncio

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="도움말", aliases=["help"])
    async def _help(self, ctx):
        embed = discord.Embed(title="도움말", description="접두사: ``?``")
        embed.add_field(
            name="급식",
            value="설명:해당학교의 급식정보를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다.\n인자값: 학교명(핗수) 날짜(선택)\n예시:\n?급식 인천기계공업고등학교\n?급식 인천기계공업고등학교 20200810",
        )
        embed.add_field(
            name="시간표",
            value="설명:해당학교의 시간표를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다. 현재 고등학교는 가져올수 없습니다.\n인자값: 학교명(핗수) 학년(필수) 반(필수) 날짜(선택)\n예시:\n?시간표 구월중학교 2 1\n?시간표 구월중학교 2 1 20200810",
        )
        embed.add_field(
            name="학사일정",
            value="설명:해당학교의 학사정보를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다.\n인자값: 학교명(핗수) 날짜(선택)\n예시:\n?학사일정 인천기계공업고등학교\n?학사일정 인천기계공업고등학교 20200808",
        )
        embed.add_field(
            name="게시물",
            value="설명:헤당학교의 아이엠스쿨 게시물을 가져옵니다.\n인자값: 학교명(핗수)\n예시:\n?게시물 인천기계공업고등학교",
        )

        await ctx.send(embed=embed)
