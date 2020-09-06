import re

import discord
from discord.ext import commands

from database import User
from utils import is_mobile

POSITIVE = [
    "네",
    "예",
    "YES",
    "true",
    "T",
    "Y",
    "True",
    "TRUE",
    "Yes",
    "yes",
    "공",
    "공개",
]

NEGATIVE = [
    "아니요",
    "아니오",
    "NO",
    "false",
    "F",
    "N",
    "False",
    "FALSE",
    "No",
    "no",
    "비공",
    "비공개",
]


class Setting(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(name="설정")
    async def _setting(self, ctx, key: str, *, value: str):
        """
        설명:학교 정보와 공개 여부를 설정합니다.
        인자값: 키(필수) 값(필수)
        예시:
        ?설정 학교 E10|7310100 1 1
        ?설정 공개 아니요
        """

        if key == "학교":  # F10|7401249|mis <학년> <반>
            Value = re.match(
                r"(B10|C10|D10|E10|F10|G10|H10|I10|J10|K10|M10|N10|P10|Q10|R10|S10|T10|V10)\|([0-9]{7})\|(els|mis|his|sps)\s([0-9]{1})\s([0-9]{1,2})",
                value,
                flags=re.I,
            )
            if not Value:
                return await ctx.send(
                    embed=discord.Embed(title="올바른 정보를 입력해주세요"),
                    mobile=is_mobile(ctx.author),
                )

            Data = (await User.get_or_create(id=ctx.author.id))[0]
            Data.neis_ae = Value.group(1)
            Data.neis_se = Value.group(2)
            Data.school_type = Value.group(3)
            Data.grade = int(Value.group(4))
            Data.class_ = int(Value.group(5))

            await Data.save()

            return await ctx.send(
                embed=discord.Embed(title="학교 정보가 설정되었습니다."),
                mobile=is_mobile(ctx.author),
            )
        if key == "공개":  # 공개|비공개
            Data = await User.get_or_none(id=ctx.author.id)

            if not Data:
                return await ctx.send(
                    embed=discord.Embed(title="학교를 먼저 설정해주세요!"),
                    mobile=is_mobile(ctx.author),
                )

            if value in POSITIVE:
                Data.public = True
            elif value in NEGATIVE:
                Data.public = False
            else:
                return await ctx.send(
                    embed=discord.Embed(title="올바른 정보를 입력해주세요"),
                    mobile=is_mobile(ctx.author),
                )

            await Data.save()

            return await ctx.send(
                embed=discord.Embed(title="학교 공개 여부가 설정되었습니다."),
                mobile=is_mobile(ctx.author),
            )
        else:
            return await ctx.send(
                embed=discord.Embed(title="설정할 수 없는 항목입니다."),
                mobile=is_mobile(ctx.author),
            )


def setup(Bot):
    Bot.add_cog(Setting(Bot))
