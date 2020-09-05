import re

import discord
from discord.ext import commands

from schoolbot import db


class Setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="설정")
    async def _setting(self, ctx, key: str = None, *, value: str = None):
        if key and value:
            args = re.split(r"||\s", value)
            if key == "학교":
                if len(args) < 5:  # I'm sad because of hardcoding...
                    return await ctx.send(embed=discord.Embed(title="올바른 정보를 입력해주세요"))
                if args[3].isdigit() and args[4].isdigit():
                    Query = {
                        "id": ctx.author.id,
                        "neis_ae": args[0],
                        "neis_se": args[1],
                        "grade": int(args[3]),
                        "class_nm": int(args[4]),
                        "class": args[2],
                    }

                    if await db.get_user_data(ctx.author.id):
                        await db.update_school(**Query)
                    else:
                        await db.create_user_data(**Query)
                    return await ctx.send(embed=discord.Embed(title="학교 정보가 설정되었습니다."))
                else:
                    return await ctx.send(
                        embed=discord.Embed(title="잘못된값을 주셨습니다. 처음부터 다시 시도해주세요.")
                    )
            elif key == "공개":
                user_data = await db.get_user_data(ctx.author.id)
                if user_data:
                    if value in [
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
                    ]:
                        public = 1
                    elif value in [
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
                    ]:
                        public = 0
                    else:
                        raise ValueError

                    await db.change_public(ctx.author.id, public)
                    return await ctx.send(
                        embed=discord.Embed(title="학교 공개 여부가 설정되었습니다.")
                    )
                else:
                    return await ctx.send(embed=discord.Embed(title="학교를 먼저 설정해주세요!"))

        else:
            return await ctx.send(embed=discord.Embed(title="올바른 정보를 입력해주세요"))
