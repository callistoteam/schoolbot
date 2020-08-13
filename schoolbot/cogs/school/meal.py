import os
import asyncio

# import traceback
# import uuid

import neispy
import discord
from discord.ext import commands


class Meal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="급식")
    async def _meal(self, ctx, school_name: str, date: int = None):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다 잠시만 기다려주세요."))
        neis = neispy.AsyncClient(os.environ["TOKEN"])
        try:
            scinfo = await neis.schoolInfo(SCHUL_NM=school_name, rawdata=True)
        except Exception as e:
            if str(e.__class__.__name__) == "DataNotFound":
                return await msg.edit(
                    embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
                )
            else:
                # str(uuid.uuid1())
                # traceback.format_exc()
                return await msg.edit(
                    embed=discord.Embed(title="알수없는 오류입니다", description=f"{e}")
                )
        if len(scinfo.data) > 1:
            school_name_list = [school_name["SCHUL_NM"] for school_name in scinfo.data]
            school_name_list_with_num = [
                str(index) + ". " + school_names
                for index, school_names in enumerate(school_name_list, 1)
            ]
            await msg.edit(
                embed=discord.Embed(
                    title="여러개의 검색결과입니다. 다음중 선택해주세요.",
                    description="\n".join(school_name_list_with_num),
                )
            )

            def check(m):
                return m.author == ctx.author

            try:
                response = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await msg.edit(
                    embed=discord.Embed(title="시간 초과입니다. 처음부터 다시 시도해주세요.")
                )
            else:
                fetch_msg = await ctx.fetch_message(response.id)
                try:
                    num = int(fetch_msg.content) - 1
                except ValueError:
                    return await msg.edit(
                        embed=discord.Embed(title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.")
                    )
                else:
                    choice = scinfo.data[num]
                    AE = choice["ATPT_OFCDC_SC_CODE"]
                    SE = choice["SD_SCHUL_CODE"]
        else:
            choice = scinfo.data[0]
            AE = choice["ATPT_OFCDC_SC_CODE"]
            SE = choice["SD_SCHUL_CODE"]

        try:
            if date is None:
                scmeal = await neis.mealServiceDietInfo(AE, SE)
            else:
                scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        except Exception as e:
            if str(e.__class__.__name__) == "DataNotFound":
                return await msg.edit(
                    embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
                )
            else:
                # str(uuid.uuid1())
                # traceback.format_exc()
                return await msg.edit(
                    embed=discord.Embed(title="알수없는 오류입니다", description=f"{e}")
                )

        meal_day = str(scmeal.MLSV_YMD)
        meal = scmeal.DDISH_NM.replace("<br/>", "\n")
        await msg.edit(
            embed=discord.Embed(
                title=f"{scmeal.SCHUL_NM}의 급식입니다.\n\n{meal_day[0:4]}년 {meal_day[4:6]}월 {meal_day[6:8]}일",
                description=meal,
            )
        )

