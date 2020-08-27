import asyncio
import os

import neispy
from neispy import DataNotFound
import discord
from discord.ext import commands
import urllib.parse
import aiohttp

from schoolbot import db


class Meal(commands.Cog):
    def __init__(self, bot, apikey):
        self.bot = bot
        self.neis = neispy.AsyncClient(apikey)

    async def render_meal_image(self, meals):
        async with aiohttp.ClientSession() as session:
            meals = "&meal=".join([urllib.parse.quote(x) for x in meals.split("<br/>")])
            async with session.post(
                f"https://api.schoolbot.callisto.team/render/?meal={meals}",
                headers={"Authorization": os.environ["MEAL_API_KEY"]},
            ) as response:
                return await response.json()

    @commands.command(name="급식")
    async def _meal(self, ctx, school_name: str = None, date: int = None):
        msg = await ctx.send(
            embed=discord.Embed(
                title="정보를 요청합니다 잠시만 기다려주세요.", colour=discord.Colour.blurple()
            )
        )
        user_data = await db.get_user_data(ctx.author.id)
        if user_data and (
            (date == None and school_name == None)
            or (school_name and school_name.isdigit())
        ):
            AE = user_data[1]
            SE = user_data[2]
            if school_name and school_name.isdigit():
                date = int(school_name)
            try:
                if not date:
                    scmeal = await self.neis.mealServiceDietInfo(AE, SE)
                else:
                    scmeal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
            except DataNotFound:
                return await msg.edit(
                    embed=discord.Embed(
                        title="정보가 없습니다. 확인하신후 다시 요청하세요", colour=discord.Colour.red()
                    )
                )

            meal_day = str(scmeal.MLSV_YMD)
            await msg.edit(
                embed=discord.Embed(
                    title=f"{scmeal.SCHUL_NM}의 급식입니다.", colour=0x2E3136,
                ).add_field(
                    name=f"{meal_day[0:4]}년 {meal_day[4:6]}월 {meal_day[6:8]}일",
                    value=scmeal.DDISH_NM.replace("<br/>", "\n"),
                )
            )
        else:
            if school_name:
                try:
                    scinfo = await self.neis.schoolInfo(
                        SCHUL_NM=school_name, rawdata=True
                    )
                except DataNotFound:
                    return await msg.edit(
                        embed=discord.Embed(
                            title="정보가 없습니다. 확인하신후 다시 요청하세요",
                            colour=discord.Colour.red(),
                        )
                    )
                if len(scinfo.data) > 1:
                    school_name_list = [
                        school_name["SCHUL_NM"] for school_name in scinfo.data
                    ]
                    school_name_list_with_num = [
                        str(index) + ". " + school_names
                        for index, school_names in enumerate(school_name_list, 1)
                    ]
                    await msg.edit(
                        embed=discord.Embed(
                            title="여러개의 검색결과입니다. 다음중 선택해주세요.",
                            description="\n".join(school_name_list_with_num),
                            colour=discord.Colour.blurple(),
                        )
                    )

                    try:
                        response = await self.bot.wait_for(
                            "message",
                            check=lambda m: m.author == ctx.author
                            and m.channel == ctx.channel,
                            timeout=30,
                        )
                    except asyncio.TimeoutError:
                        return await msg.edit(
                            embed=discord.Embed(
                                title="시간 초과입니다. 처음부터 다시 시도해주세요.",
                                colour=discord.Colour.red(),
                            )
                        )
                    else:
                        if response.content.isdigit():
                            num = response.content - 1
                        else:
                            return await msg.edit(
                                embed=discord.Embed(
                                    title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.",
                                )
                            )
                        choice = scinfo.data[num]
                        AE = choice["ATPT_OFCDC_SC_CODE"]
                        SE = choice["SD_SCHUL_CODE"]
                else:
                    choice = scinfo.data[0]
                    AE = choice["ATPT_OFCDC_SC_CODE"]
                    SE = choice["SD_SCHUL_CODE"]
            else:
                return await msg.edit(
                    embed=discord.Embed(title="학교명을 입력해주세요")
                )

            try:
                if not date:
                    scmeal = await self.neis.mealServiceDietInfo(AE, SE)
                else:
                    scmeal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
            except DataNotFound:
                return await msg.edit(
                    embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
                )

            meal_day = str(scmeal.MLSV_YMD)
            meal_image = await self.render_meal_image(scmeal.DDISH_NM)
            await msg.edit(
                embed=discord.Embed(title=f"{scmeal.SCHUL_NM}의 급식입니다.", colour=0x2E3136)
                .set_image(url=meal_image["url"])
                .add_field(
                    name=f"{meal_day[0:4]}년 {meal_day[4:6]}월 {meal_day[6:8]}일",
                    value=scmeal.DDISH_NM.replace("<br/>", "\n"),
                )
            )
