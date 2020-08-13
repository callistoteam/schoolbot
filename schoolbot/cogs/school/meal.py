import os
import asyncio

import neispy
import discord
from discord.ext import commands

neis = neispy.AsyncClient(os.environ["API_KEY"])


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="급식")
    async def _meal(self, ctx, school_name: str):
        scinfo = await neis.schoolInfo(SCHUL_NM=school_name, rawdata=True)
        if len(scinfo.data) > 1:
            school_name_list = [school_name["SCHUL_NM"] for school_name in scinfo.data]
            school_name_list_with_num = [str(index) + ". " + school_names for index, school_names in enumerate(school_name_list, 1)]
            await ctx.send("\n".join(school_name_list_with_num))
            def check2(m):
                return m.user == ctx.author
            try:
                respon = await self.bot.wait_for('message', check=check2, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("시간 초과입니다.")
            else:
                fetch_msg = await ctx.fetch_message(respon.id)
                try:
                    num = int(fetmsg.content) - 1
                except ValueError:
                    return await ctx.send("잘못된 값을 주셧습니다. 처음부터 다시 시도해주세요")
                else:
                    choice = scinfo[num]
                    AE = choice["ATPT_OFCDC_SC_CODE"]
                    SE = choice["SD_SCHUL_CODE"]
        else:
            AE = scinfo.ATPT_OFCDC_SC_CODE
            SE = scinfo.SD_SCHUL_CODE

        scmeal = await neis.mealServiceDietInfo(AE,SE)
        meal = scmeal.DDISH_NM.replace('<br/>', '\n')
        await ctx.send(meal)
            
            