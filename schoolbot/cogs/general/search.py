import asyncio
import datetime
import os
import neispy
from neispy import DataNotFound
import discord
from discord.ext import commands


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.neis = neispy.AsyncClient(os.environ["API_KEY"])

    @commands.command(name="검색")
    async def _search(self, ctx, schoolname: str = None):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다 잠시만 기다려주세요."))
        if schoolname:
            try:
                scinfo = await self.neis.schoolInfo(SCHUL_NM=schoolname, rawdata=True)
            except DataNotFound:
                return await msg.edit(
                    embed=discord.Embed(title="정보가 없습니다. 확인하신후 다시 요청하세요")
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
            return await msg.edit(
                embed=discord.Embed(title="학교명을 입력해주세요")
            )  # 쿼리문 쓰고 지워도 되는거

        if "초등학교" in SN:
            scclass = "els"
        elif "중학교" in SN:
            scclass = "mis"
        elif "고등학교" in SN:
            scclass = "his"

        embed = discord.Embed(title="검색 정보", description="")
        embed.add_field(
            name=choice["ORG_RDNMA"], value=choice["SCHUL_NM"], inline=False
        )
        embed.add_field(name="학교 ID", value=f"{AE}{SE}")
        embed.add_field(name="유형", value=choice["SCHUL_KND_SC_NM"])
        embed.add_field(
            name="설립일",
            value=datetime.datetime.strptime(choice["FOND_YMD"], "%Y%m%d").strftime(
                "%Y-%m-%d"
            ),
        )
        embed.add_field(name="남녀 구분", value=choice["COEDU_SC_NM"])
        embed.add_field(name="우편번호", value=choice["ORG_RDNZC"])
        embed.add_field(
            name="전화번호 / 팩스번호", value=f"{choice['ORG_TELNO']} / {choice['ORG_FAXNO']}"
        )
        embed.add_field(name="홈페이지", value=choice["HMPG_ADRES"])
        embed.add_field(name="설립 유형", value=choice["FOND_SC_NM"])
        embed.add_field(
            name="검색된 정보가 일치한가요?",
            value=f"`?설정 학교 {AE}|{SE}|{scclass} <학년> <반>`를 입력해서 학교를 설정할 수 있습니다!",
        )
        await msg.edit(embed=embed)
