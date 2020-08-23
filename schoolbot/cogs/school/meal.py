import asyncio

import neispy
import os
from neispy import DataNotFound
import discord
from discord.ext import commands
import aiohttp


class Meal(commands.Cog):
    def __init__(self, bot, apikey):
        self.bot = bot
        self.neis = neispy.AsyncClient(apikey)

    async def render_meal_image(self, meals):
        async with aiohttp.ClientSession() as session:
            meals = '&meal='.join(meals.split('<br/>'))
            async with session.post(f"https://api.schoolbot.callisto.team/render/?meal={meals}", headers={ "Authorization":  os.environ["MEAL_API_KEY"] }) as response:
                return await response.json()

    @commands.command(name="급식")
    async def _meal(self, ctx, school_name: str = None, date: int = None):
        msg = await ctx.send(
            embed=discord.Embed(
                title="정보를 요청합니다 잠시만 기다려주세요.", colour=discord.Colour.blurple()
            )
        )
        if school_name:
            try:
                scinfo = await self.neis.schoolInfo(SCHUL_NM=school_name, rawdata=True)
            except DataNotFound:
                return await msg.edit(
                    embed=discord.Embed(
                        title="정보가 없습니다. 확인하신후 다시 요청하세요", colour=discord.Colour.red()
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
                        num = int(response.content) - 1
                    else:
                        return await msg.edit(
                            embed=discord.Embed(
                                title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.",
                                colour=discord.Colour.red(),
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
            # 대충 여따가 쿼리문 적으면 된다는 주석
            # AE = 대충 교육청코드
            # SE = 대충 표준학교코드
            return await msg.edit(
                embed=discord.Embed(title="학교명을 입력해주세요", colour=discord.Colour.red(),)
            )  # 쿼리문 쓰고 지워도 되는거

        try:
            if not date:
                scmeal = await self.neis.mealServiceDietInfo(AE, SE)
            else:
                scmeal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        except DataNotFound:
            return await msg.edit(
                embed=discord.Embed(
                    title="정보가 없습니다. 확인하신후 다시 요청하세요", colour=discord.Colour.red(),
                )
            )

        meal_day = str(scmeal.MLSV_YMD)
        meal_image = await self.render_meal_image(scmeal.DDISH_NM)
        await msg.edit(
            embed=discord.Embed(
                title=f"{scmeal.SCHUL_NM}의 급식입니다.", colour=0x2E3136
            ).set_image(url=meal_image['url']).add_field(
                name=f"{meal_day[0:4]}년 {meal_day[4:6]}월 {meal_day[6:8]}일",
                value=scmeal.DDISH_NM.replace("<br/>", "\n"),
            )
        )
