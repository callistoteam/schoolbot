import os
import traceback
import uuid


import schoolbot
from utils.kst import kst_sft
import discord
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 값이 부족합니다. `?도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 지정한 값이 잘못되었습니다. `?도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send("관리자만 사용하실수있는 명령어입니다.", delete_after=5)
        else:
            trace_uuid = str(uuid.uuid4())
            await ctx.send(
                embed=discord.Embed(
                    title="알 수 없는 오류가 발생했습니다.",
                    description=f"다음 정보를 개발자에게 알려주시면 문제해결에 도움이됩니다.\n**UUID**: ``{trace_uuid}``",
                    colour=discord.Color.red(),
                )
            )

            trace_embed = discord.Embed(
                title=f"Unexpected Error in schoolbot\n**UUID**: ``{trace_uuid}``",
                description=f"**Version**: ``{schoolbot.__version__}``\n"
                f"**User**: ``{ctx.author}`` (``{ctx.author.id}``)\n"
                f"**Guild**: ``{ctx.author.guild}`` (``{ctx.author.guild.id}``)\n"
                f"**Channel**: ``{ctx.channel}`` (``{ctx.channel.id}``)\n"
                f"**Command**: ``{ctx.command}``\n"
                f"**Bot Permission**: ``{ctx.guild.me.guild_permissions.value}``",
            )
            trace_embed.set_footer(text=kst_sft())
            if not error.__cause__:
                trace_embed.add_field(
                    name="Traceback:",
                    value=f"```py\n{''.join(traceback.format_exception(type(error), error, error.__traceback__, limit=3))}\n```",
                )
            else:
                trace_embed.add_field(
                    name="Traceback:",
                    value=f"```py\n{''.join(traceback.format_exception(type(error.__cause__), error.__cause__, error.__cause__.__traceback__, limit=3))}\n```",
                )
            channel = await self.bot.fetch_channel(os.environ["channel_id"])
            await channel.send(embed=trace_embed)
