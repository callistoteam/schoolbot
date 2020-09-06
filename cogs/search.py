from datetime import datetime

import discord
from discord.ext import commands

SCHUL_KND_SC_NM = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class Search(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="검색")
    async def _search(self, ctx, schoolname: str = None):
        """
        설명:학교 설정에 필요한 학교 정보를 검색합니다.
        인자값: 학교명(필수)
        예시:
        ?검색 인천기계공업고등학교
        """

        if not schoolname:
            return await ctx.send(
                embed=discord.Embed(
                    title="학교명을 입력 해주시기 바랍니다.", colur=discord.Colour.red()
                )
            )

        School = await self.Bot.search_school(ctx, schoolname)
        if not School:
            return

        AE, SE, SCHOOL_TYPE = (
            School.ATPT_OFCDC_SC_CODE,
            School.SD_SCHUL_CODE,
            SCHUL_KND_SC_NM[School.SCHUL_KND_SC_NM],
        )

        await ctx.send(
            embed=discord.Embed(title="검색 정보")
            .add_field(name=School.ORG_RDNMA, value=School.SCHUL_NM, inline=False)
            .add_field(name="학교 ID", value=f"{AE}{SE}")
            .add_field(name="유형", value=School.SCHUL_KND_SC_NM)
            .add_field(
                name="설립일",
                value=datetime.strptime(School.FOND_YMD, "%Y%m%d").strftime("%Y-%m-%d"),
            )
            .add_field(name="남녀 구분", value=School.COEDU_SC_NM)
            .add_field(name="우편번호", value=School.ORG_RDNZC)
            .add_field(
                name="전화번호 / 팩스번호", value=f"{School.ORG_TELNO} / {School.ORG_FAXNO}"
            )
            .add_field(name="홈페이지", value=School.HMPG_ADRES)
            .add_field(name="설립 유형", value=School.FOND_SC_NM)
            .add_field(
                name="검색된 정보가 일치한가요?",
                value=f"`{self.Bot.command_prefix}설정 학교 {AE}|{SE}|{SCHOOL_TYPE} <학년> <반>`를 입력해서 학교를 설정할 수 있습니다!",
            )
        )


def setup(Bot):
    Bot.add_cog(Search(Bot))
