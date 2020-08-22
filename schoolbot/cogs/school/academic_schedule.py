import asyncio

import neispy
from neispy import DataNotFound
import discord
from discord.ext import commands


class AcademicSchedule(commands.Cog):
    def __init__(self, bot, apikey):
        self.bot = bot
        self.neis = neispy.AsyncClient(apikey)

    @commands.command(name="학사일정")
    async def _academic_schedule(self, ctx, schoolname: str = None, date: int = None):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다 잠시만 기다려주세요."))
        if schoolname:
            try:
                scinfo = await self.neis.schoolInfo(SCHUL_NM=schoolname, rawdata=True)
            except Exception as e:
                if isinstance(e, DataNotFound):
                    return await msg.edit(
                        embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
                    )
                else:
                    return await msg.edit(
                        embed=discord.Embed(title="알수없는 오류입니다", description=f"{e}")
                    )
            if scinfo.data:
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
                        embed=discord.Embed(title="시간 초과입니다. 처음부터 다시 시도해주세요.")
                    )
                else:
                    if response.content.isdigit():
                        num = response.content - 1
                    else:
                        return await msg.edit(
                            embed=discord.Embed(title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.")
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
                embed=discord.Embed(title="학교명을 입력해주세요")
            )  # 쿼리문 쓰고 지워도 되는거

        try:
            if not date:
                scacca = await self.neis.SchoolSchedule(AE, SE)
            else:
                scacca = await self.neis.SchoolSchedule(AE, SE, AA_YMD=date)
        except DataNotFound:
            return await msg.edit(embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요"))

        acca_day = scacca.AA_YMD
        await msg.edit(
            embed=discord.Embed(
                title=f"{scacca.SCHUL_NM}의 학사일정입니다.\n\n{acca_day[0:4]}년 {acca_day[4:6]}월 {acca_day[6:8]}일",
                description=f"**{scacca.EVENT_NM}**\n{scacca.CNTNT if scacca.CNTNT else '해당 학사일정의 내용이 없습니다.'}",
            )
        )
