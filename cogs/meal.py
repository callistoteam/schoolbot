import os
import discord
from discord.ext import commands
from datetime import datetime

import aiohttp
import urllib.parse
import neispy
from database import User


class Meal(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    async def __get_meal_image(self, meals):
        async with aiohttp.ClientSession() as session:
            meals = "&meal=".join([urllib.parse.quote(x) for x in meals.split("<br/>")])
            async with session.post(
                f"https://api.schoolbot.callisto.team/render/?meal={meals}",
                headers={"Authorization": os.environ["MEAL_API_KEY"]},
            ) as res:
                return (await res.json())["url"]

    @commands.command(name="급식")
    async def _meal(self, ctx, schoolname: str = None, date: str = neispy.now()):
        """
        설명:해당학교의 급식정보를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다.
        인자값: 학교명(미설정시 필수) 날짜(선택)
        예시:
        ?급식 인천기계공업고등학교
        ?급식 인천기계공업고등학교 20200810
        """

        if schoolname and schoolname.isdigit():
            schoolname, date = None, schoolname

        if schoolname:
            School = await self.Bot.search_school(ctx, schoolname)
            if not School:
                return

            AE, SE = School.ATPT_OFCDC_SC_CODE, School.SD_SCHUL_CODE
        else:
            Data = await User.get_or_none(id=ctx.author.id)
            if not Data:
                return await ctx.send(
                    embed=discord.Embed(
                        title="학교명을 입력 해주시기 바랍니다.", colur=discord.Colour.red()
                    )
                )

            AE, SE = Data.neis_ae, Data.neis_se

        try:
            meal = await self.Bot.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        except neispy.DataNotFound:
            return await ctx.send(
                embed=discord.Embed(
                    title="해당하는 날짜에 급식이 없는거 같습니다.", colur=discord.Colour.red()
                )
            )
        else:
            meal = meal[0]

        embed = discord.Embed(
            title=f"{meal.SCHUL_NM}의 급식입니다.", colour=0x2E3136
        ).add_field(
            name=datetime.strptime(meal.MLSV_YMD, "%Y%m%d").strftime("%Y년 %m월 %d일"),
            value=meal.DDISH_NM.replace("<br/>", "\n"),
        )

        message = await ctx.send(embed=embed)

        embed.set_image(url=await self.__get_meal_image(meal.DDISH_NM))

        await message.edit(embed=embed)


def setup(Bot):
    Bot.add_cog(Meal(Bot))
