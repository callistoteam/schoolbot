from datetime import datetime

import discord
import neispy
from discord.ext import commands

from database import User
from utils import is_mobile


class Schedule(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="학사일정")
    async def _schedule(self, ctx, schoolname: str = None, date: str = neispy.now()):
        """
        설명:해당학교의 학사정보를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다.
        인자값: 학교명(미설정시 필수) 날짜(선택)
        예시:
        ?학사일정 인천기계공업고등학교
        ?학사일정 인천기계공업고등학교 20200808
        """

        if schoolname and schoolname.isdigit():
            schoolname, date = None, schoolname

        if schoolname:
            School = await self.Bot.search_school(ctx, schoolname)
            if not School:
                return

            Data, AE, SE = None, School.ATPT_OFCDC_SC_CODE, School.SD_SCHUL_CODE
        else:
            Data = await User.get_or_none(id=ctx.author.id)
            if not Data:
                return await ctx.send(
                    embed=discord.Embed(
                        title="학교명을 입력해주세요.", colur=discord.Colour.red()
                    ),
                    mobile=is_mobile(ctx.author),
                )

            AE, SE = Data.neis_ae, Data.neis_se

        try:
            schedule = await self.Bot.neis.SchoolSchedule(AE, SE, AA_YMD=date)
        except neispy.DataNotFound:
            return await ctx.send(
                datetime.strptime(date, "%Y%m%d").strftime("%m월 %d일")
                + "의 학사일정을 찾을 수 없습니다.",
                mobile=is_mobile(ctx.author),
            )
        else:
            schedule = schedule[0]

        await ctx.send(
            embed=discord.Embed(
                title=f"{schedule.SCHUL_NM if not Data or Data.public else '`학교 비공개`'}의 학사일정입니다",
                description=datetime.strptime(schedule.AA_YMD, "%Y%m%d").strftime(
                    "%Y년 %m월 %d일"
                ),
                colour=0x2E3136,
            ).add_field(
                name=f"**{schedule.EVENT_NM}**",
                value=f"{schedule.EVENT_CNTNT if schedule.EVENT_CNTNT else '해당 학사일정의 내용이 없습니다.'}",
            ),
            mobile=is_mobile(ctx.author),
        )


def setup(Bot):
    Bot.add_cog(Schedule(Bot))
