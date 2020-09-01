import asyncio

import neispy
from neispy import DataNotFound
import discord
from discord.ext import commands

from schoolbot import db


class TimeTable(commands.Cog):
    def __init__(self, bot, apikey):
        self.bot = bot
        self.neis = neispy.Client(apikey)

    @commands.command(name="시간표")
    async def _timetable(
        self,
        ctx,
        school_name: str = None,
        grade: int = None,
        class_nm: int = None,
        date: int = None,
    ):
        if school_name and school_name.isdigit():
            if len(school_name) == 8:
                date = int(school_name)
            elif class_nm:
                date = class_nm
                class_nm = grade
                grade = school_name
            else:
                class_nm = grade
                grade = school_name
        if not grade or not class_nm:
            return await ctx.send(
                embed=discord.Embed(
                    title="학년과 반 정보를 입력해주세요!", colour=discord.Colour.red()
                )
            )
        user_data = await db.get_user_data(ctx.author.id)
        if user_data and not school_name:
            msg = await ctx.send(
                embed=discord.Embed(
                    title="정보를 요청합니다 잠시만 기다려주세요.", colour=discord.Colour.blurple()
                )
            )
            AE = user_data["neis_ae"]
            SE = user_data["neis_se"]
            if not grade:
                grade = user_data["grade"]
            if not class_nm:
                class_nm = user_data["class_nm"]
            scclass = user_data["class"]
            if scclass != "his":
                try:
                    if not date:
                        sctimetable = await self.neis.timeTable(
                            scclass, AE, SE, GRADE=grade, CLASS_NM=class_nm
                        )
                    else:
                        sctimetable = await self.neis.timeTable(
                            scclass,
                            AE,
                            SE,
                            ALL_TI_YMD=date,
                            TI_FROM_YMD=date,
                            TI_TO_YMD=date,
                            GRADE=grade,
                            CLASS_NM=class_nm,
                        )
                except DataNotFound:
                    return await msg.edit(
                        embed=discord.Embed(
                            title="정보가 없습니다. 확인하신 후 다시 요청하세요",
                            colour=discord.Colour.red(),
                        )
                    )

                tt_day = str(sctimetable[0].ALL_TI_YMD)
                await msg.edit(
                    embed=discord.Embed(
                        title=sctimetable[0].SCHUL_NM,
                        colour=0x2E3136,
                    )
                ).add_field(
                    name=f"{tt_day[0:4]}년 {tt_day[4:6]}월 {tt_day[6:8]}",
                    value="\n".join([i.ITRT_CNTNT for i in sctimetable]),
                )
            else:
                return await msg.edit(
                    embed=discord.Embed(
                        title="죄송합니다. 현재 고등학교는 지원하지 않습니다.",
                        colour=discord.Colour.red(),
                    )  # 고등학교 지원할때 빼면됨
                )

        else:
            if school_name:
                msg = await ctx.send(
                    embed=discord.Embed(
                        title="정보를 요청합니다 잠시만 기다려주세요.", colour=discord.Colour.blurple()
                    )
                )
                try:
                    scinfo = await self.neis.schoolInfo(SCHUL_NM=school_name)
                except DataNotFound:
                    return await msg.edit(
                        embed=discord.Embed(
                            title="정보가 없습니다. 확인하신후 다시 요청하세요",
                            colour=discord.Colour.red(),
                        )
                    )
                if len(scinfo) > 1:
                    school_name_list = [school_name.SCHUL_NM for school_name in scinfo]
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
                                colour=discord.Colour.blurple(),
                            )
                        )
                    else:
                        if response.content.isdigit():
                            num = int(response.content) - 1
                        else:
                            return await msg.edit(
                                embed=discord.Embed(
                                    title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.",
                                )
                            )
                        AE = scinfo[num].ATPT_OFCDC_SC_CODE
                        SE = scinfo[num].SD_SCHUL_CODE
                        SN = scinfo[num].SCHUL_NM
                else:
                    AE = scinfo[0].ATPT_OFCDC_SC_CODE
                    SE = scinfo[0].SD_SCHUL_CODE
                    SN = scinfo[0].SCHUL_NM
            else:
                # 대충 여따가 쿼리문 적으면 된다는 주석
                # AE = 대충 교육청코드
                # SE = 대충 표준학교코드
                # scclass = 대충 초 중 고 고르는거
                return await ctx.send(
                    embed=discord.Embed(
                        title="학교명을 입력해주세요", colour=discord.Colour.blurple()
                    )
                )  # 쿼리문 쓰고 지워도 되는거

            # if scclass:
            #    pass
            if "초등학교" in SN:
                scclass = "els"
            elif "중학교" in SN:
                scclass = "mis"
            elif "고등학교" in SN:
                return await msg.edit(
                    embed=discord.Embed(
                        title="죄송합니다. 현재 고등학교는 지원하지 않습니다.",
                        colour=discord.Colour.blurple(),
                    )  # 고등학교 지원할때 빼면됨
                )
            else:
                return await msg.edit(
                    embed=discord.Embed(
                        title="죄송합니다. 지원하지 않는 학교입니다.", colour=discord.Colour.red()
                    )
                )
            try:
                if not date:
                    sctimetable = await self.neis.timeTable(
                        scclass, AE, SE, GRADE=grade, CLASS_NM=class_nm
                    )
                else:
                    sctimetable = await self.neis.timeTable(
                        scclass,
                        AE,
                        SE,
                        ALL_TI_YMD=date,
                        TI_FROM_YMD=date,
                        TI_TO_YMD=date,
                        GRADE=grade,
                        CLASS_NM=class_nm,
                    )
            except DataNotFound:
                return await msg.edit(
                    embed=discord.Embed(
                        title="정보가 없습니다. 확인하신 후 다시 요청하세요", colour=discord.Colour.red()
                    )
                )
            tt_day = str(sctimetable[0].ALL_TI_YMD)
            await msg.edit(
                embed=discord.Embed(
                    title=sctimetable[0].SCHUL_NM,
                    colour=0x2E3136,
                )
            ).add_field(
                name=f"{tt_day[0:4]}년 {tt_day[4:6]}월 {tt_day[6:8]}일",
                value="\n".join([i.ITRT_CNTNT for i in sctimetable]),
            )
