import re
from datetime import datetime

import discord
import neispy
from discord.ext import commands

from database import User
from utils import is_mobile

SCHUL_KND_SC_NM = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class TimeTable(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="시간표")
    async def _time_table(
        self,
        ctx,
        a: str = None,
        b: str = None,
        c: str = None,
        d: str = None,
        e: str = None,
        f: str = neispy.now(),
    ):
        """
        설명:해당학교의 시간표를 알려줍니다. 날짜가 주어지지 않았을경우 현재 날짜로 가져옵니다. 현재 고등학교는 가져올수 없습니다.
        인자값: 학교명(미설정시 필수) 학년(미설정시 필수) 반(미설정시 필수) 날짜(선택)
        예시:
        ?시간표 구월중학교 2 1
        ?시간표 구월중학교 2 1 20200810
        """

        schoolname = grade = class_ = AFLCO = MAJOR = date = None
        for Data in [Item for Item in [a, b, c, d, e, f] if Item]:
            if not schoolname and re.fullmatch("[가-힣]+", Data):
                schoolname = Data
            elif not grade and re.fullmatch("[1-6]{1}", Data):
                grade = Data
            elif not class_ and re.fullmatch("[0-9]{1,2}", Data):
                class_ = Data
            elif not AFLCO and re.fullmatch("[가-힣]+", Data):
                AFLCO = Data
            elif not MAJOR and re.fullmatch("[가-힣]+", Data):
                MAJOR = Data
            elif not date and re.fullmatch(
                "[0-9]{8}",
                Data,
            ):
                date = Data

        if schoolname:
            School = await self.Bot.search_school(ctx, schoolname)
            if not School:
                return

            Data, AE, SE, SN = (
                None,
                School.ATPT_OFCDC_SC_CODE,
                School.SD_SCHUL_CODE,
                SCHUL_KND_SC_NM[School.SCHUL_KND_SC_NM],
            )

            if not (grade and class_):
                return await ctx.send("학년과 반을 입력해주세요", mobile=is_mobile(ctx.author))

            if SN == "his" and not (AFLCO and MAJOR):
                return await ctx.send("계열과 학과를 입력해주세요", mobile=is_mobile(ctx.author))
        else:
            Data = await User.get_or_none(id=ctx.author.id)
            if not Data:
                return await ctx.send(
                    embed=discord.Embed(
                        title="학교명을 입력 해주세요.", colur=discord.Colour.red()
                    ),
                    mobile=is_mobile(ctx.author),
                )

            AE, SE, SN, AFLCO, MAJOR = (
                Data.neis_ae,
                Data.neis_se,
                Data.school_type,
                Data.aflco,
                Data.major,
            )

            if not grade:
                grade = Data.grade
            if not class_:
                class_ = Data.class_

        try:
            timetable = await self.Bot.neis.timeTable(
                SN,
                AE,
                SE,
                ALL_TI_YMD=date,
                TI_FROM_YMD=date,
                TI_TO_YMD=date,
                GRADE=grade,
                ORD_SC_NM=AFLCO,
                DDDEP_NM=MAJOR,
            )
        except neispy.DataNotFound:
            return await ctx.send(
                datetime.strptime(date, "%Y%m%d").strftime("%m월 %d일")
                + "의 시간표 정보를 찾을 수 없습니다.",
                mobile=is_mobile(ctx.author),
            )

        timetable = [time for time in timetable if int(time.CLASS_NM) == int(class_)]

        await ctx.send(
            embed=discord.Embed(
                title=timetable[0].SCHUL_NM
                if not Data or not Data.public
                else "`학교 비공개`",
                colour=0x2E3136,
            ).add_field(
                name=datetime.strptime(timetable[0].ALL_TI_YMD, "%Y%m%d").strftime(
                    "%Y년 %m월 %d일"
                ),
                value="\n".join(
                    [
                        f"{index}교시 {value.ITRT_CNTNT}"
                        for index, value in enumerate(timetable, 1)
                    ]
                ),
            ),
            mobile=is_mobile(ctx.author),
        )


def setup(Bot):
    Bot.add_cog(TimeTable(Bot))
