import asyncio
import datetime

import iamschool
from iamschool import HTTPException
import discord
from discord.ext import commands


class Article(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = iamschool.AsyncClient()

    @commands.command(name="게시물")
    async def _article(self, ctx, school_name: str = None):
        msg = await ctx.send(
            embed=discord.Embed(
                title="정보를 요청합니다 잠시만 기다려주세요.", colour=discord.Colour.blurple()
            )
        )
        if school_name:
            try:
                scinfo = await self.client.search_school(school_name)
            except HTTPException as e:
                return await msg.edit(
                    embed=discord.Embed(
                        title="HTTP 요청 오류입니다",
                        description=f"{e}",
                        colour=discord.Colour.red(),
                    )
                )
            else:
                if not scinfo:
                    return await msg.edit(
                        embed=discord.Embed(
                            title="아이엠스쿨에 등록되지 않았습니다. 확인하신후 다시 요청하세요",
                            description=" [아이엠스쿨 바로가기](https://school.iamservice.net/) ",
                            colour=discord.Colour.red(),
                        )
                    )
                else:
                    if len(scinfo) > 1:
                        school_name_list = [school_name.name for school_name in scinfo]
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

                            choice = scinfo[num]
                    else:
                        choice = scinfo[0]
        else:
            return await msg.edit(
                embed=discord.Embed(title="학교명을 입력해주세요", colour=discord.Colour.red())
            )
        try:
            scarticles = await self.client.fetch_recent_article(choice.id)
        except HTTPException as e:
            return await msg.edit(
                embed=discord.Embed(
                    title="HTTP 요청 오류입니다",
                    description=f"{e}",
                    colour=discord.Colour.red(),
                )
            )
        else:
            if not scarticles:
                return await msg.edit(
                    embed=discord.Embed(
                        title="아이엠스쿨에 게시된 게시물이 없습니다.",
                        description=" [아이엠스쿨 바로가기](https://school.iamservice.net/) ",
                        colour=discord.Colour.red(),
                    )
                )
            else:
                position = 0
                embed = discord.Embed(
                    title=scarticles[position].title,
                    description=scarticles[position].content,
                    timestamp=datetime.datetime.strptime(
                        scarticles[position].date, "%Y.%m.%d"
                    ),
                    url=scarticles[position].link,
                    colour=0x2E3136,
                )
                embed.set_author(
                    name=scarticles[position].organization_name,
                    url=f"https://school.iamservice.net/organization/{scarticles[position].organization_id}",
                    icon_url=scarticles[position].organization_logo,
                )
                embed.set_footer(
                    text=f"#{scarticles[position].group.name} • {scarticles[position].author}"
                )
                if scarticles[position].images:
                    embed.set_image(url=scarticles[position].images[0])
                await msg.edit(embed=embed)
                await msg.add_reaction("◀")
                await msg.add_reaction("⏹")
                await msg.add_reaction("▶")
                while not self.bot.is_closed():
                    try:
                        reaction, user = await self.bot.wait_for(
                            "reaction_add",
                            check=lambda reaction, user: user == ctx.author
                            and reaction.message.id == msg.id
                            and reaction.emoji in ["◀", "⏹", "▶"],
                            timeout=30,
                        )
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        break
                    else:
                        if reaction.emoji == "◀":
                            position -= 1
                        elif reaction.emoji == "⏹":
                            try:
                                await msg.clear_reactions()
                            except Exception:
                                pass
                            break
                        else:
                            position += 1
                        if position < 0:
                            position = len(scarticles) - 1
                        if position >= len(scarticles):
                            position = 0
                        embed = discord.Embed(
                            title=scarticles[position].title,
                            description=scarticles[position].content,
                            timestamp=datetime.datetime.strptime(
                                scarticles[position].date, "%Y.%m.%d"
                            ),
                            url=scarticles[position].link,
                            colour=0x2E3136,
                        )
                        embed.set_author(
                            name=scarticles[position].organization_name,
                            url=f"https://school.iamservice.net/organization/{scarticles[position].organization_id}",
                            icon_url=scarticles[position].organization_logo,
                        )
                        embed.set_footer(
                            text=f"#{scarticles[position].group.name} • {scarticles[position].author}"
                        )
                        if scarticles[position].images:
                            embed.set_image(url=scarticles[position].images[0])
                        await msg.edit(embed=embed)
                        try:
                            await msg.remove_reaction(reaction.emoji, user)
                        except Exception:
                            pass
                return
