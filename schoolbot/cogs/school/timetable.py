import asyncio

# import traceback
# import uuid

import neispy
from neispy import DataNotFound
import discord
from discord.ext import commands


class TimeTable(commands.Cog):
    def __init__(self, bot, apikey):
        self.bot = bot
        self.neis = neispy.AsyncClient(apikey)

    @commands.command(name="시간표")
    async def _timetable(
        self,
        ctx,
        school_name: str = None,
        grade: int = None,
        class_nm: int = None,
        date: int = None,
    ):
        if not grade or not class_nm:
            return await ctx.send(embed=discord.Embed(title="학년과 반정보를 입력해주세요!"))
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다 잠시만 기다려주세요."))
        if school_name:
            try:
                scinfo = await self.neis.schoolInfo(SCHUL_NM=school_name, rawdata=True)
            except Exception as e:
                if isinstance(e, DataNotFound):
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
                        SN = choice["SCHUL_NM"]
            else:
                choice = scinfo.data[0]
                AE = choice["ATPT_OFCDC_SC_CODE"]
                SE = choice["SD_SCHUL_CODE"]
                SN = choice["SCHUL_NM"]
        else:
            # 대충 여따가 쿼리문 적으면 된다는 주석
            # AE = 대충 교육청코드
            # SE = 대충 표준학교코드
            # scclass = 대충 초 중 고 고르는거
            return await msg.edit(
                embed=discord.Embed(title="학교명을 입력해주세요")
            )  # 쿼리문 쓰고 지워도 되는거

        # if scclass:
        #    pass
        if "초등학교" in SN:
            scclass = "els"
        elif "중학교" in SN:
            scclass = "mis"
        elif "고등학교" in SN:
            return await msg.edit(
                embed=discord.Embed(title="죄송합니다. 현재 고등학교는 지원하지않습니다.")  # 고등학교 지원할때 빼면됨
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
        except Exception as e:
            if isinstance(e, DataNotFound):
                return await msg.edit(
                    embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
                )
            return await msg.edit(
                embed=discord.Embed(title="알수없는 오류입니다", description=f"{e}")
            )

        tt_scname = sctimetable.data[0]["SCHUL_NM"]
        tt_day = sctimetable.data[0]["ALL_TI_YMD"]
        await msg.edit(
            embed=discord.Embed(
                title=f"{tt_scname}의 {tt_day[0:4]}년 {tt_day[4:6]}월 {tt_day[6:8]}일 시간표입니다.",
                description="\n".join([i["ITRT_CNTNT"] for i in sctimetable.data]),
            )
        )
