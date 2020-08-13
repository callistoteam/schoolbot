import os
import asyncio

import neispy
import discord
from discord.ext import commands


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="급식")
    async def _meal(self, ctx, school_name: str, date: int = None):
        msg = await ctx.send("정보를 요청합니다 잠시만 기다려주세요.")
        neis = neispy.AsyncClient(os.environ["API_KEY"])
        scinfo = await neis.schoolInfo(SCHUL_NM=school_name, rawdata=True)
        if len(scinfo.data) > 1:
            school_name_list = [school_name["SCHUL_NM"] for school_name in scinfo.data]
            school_name_list_with_num = [
                str(index) + ". " + school_names
                for index, school_names in enumerate(school_name_list, 1)
            ]
            await msg.edit("\n".join(school_name_list_with_num))

            def check(m):
                return m.author == ctx.author

            try:
                respon = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await msg.edit("시간 초과입니다.")
            else:
                fetch_msg = await ctx.fetch_message(respon.id)
                try:
                    num = int(fetch_msg.content) - 1
                except ValueError:
                    return await ctx.send("잘못된 값을 주셧습니다. 처음부터 다시 시도해주세요")
                else:
                    choice = scinfo.data[num]
                    AE = choice["ATPT_OFCDC_SC_CODE"]
                    SE = choice["SD_SCHUL_CODE"]
        else:
            choice = scinfo.data[0]
            AE = choice["ATPT_OFCDC_SC_CODE"]
            SE = choice["SD_SCHUL_CODE"]

        if date is None:
            scmeal = await neis.mealServiceDietInfo(AE, SE)
        else:
            scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)

        meal = scmeal.DDISH_NM.replace("<br/>", "\n")
        await msg.edit(meal)

