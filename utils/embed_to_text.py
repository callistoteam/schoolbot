import re

import discord


def embed_to_text(embed):
    return (
        f"**{embed.title}**\n"
        + (("<" + embed.url + ">\n") if embed.url != discord.Embed.Empty else "")
        + (
            (f"\n> " + embed.description.replace("\n", "\n> "))
            if embed.description != discord.Embed.Empty
            else ""
        )
        + "\n\n"
        + "\n\n".join(
            [
                f"**{field.name}**\n"
                + (
                    (
                        "> "
                        + re.sub(
                            "\[(.*?)\]\((.*?)\)",
                            "\g<1>: \g<2>",
                            field.value,
                        ).replace("\n", "\n> ")
                    )
                    if field.value
                    else ""
                )
                for field in embed.fields
                if field != discord.Embed.Empty
            ]
        )
        + "\n"
        + (
            ("\n" + embed.footer.text)
            if embed.footer.text != discord.Embed.Empty
            else ""
        )
        + (
            " · "
            if embed.footer != discord.Embed.Empty
            and embed.timestamp != discord.Embed.Empty
            else ""
        )
        + (
            embed.timestamp.strftime("%p %H:%M")
            if embed.timestamp != discord.Embed.Empty
            else ""
        )
    )
