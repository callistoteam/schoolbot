import discord


def embed_to_text(embed):
    return (
        f"**{embed.title}**\n"
        + ((embed.url + "\n") if embed.url != discord.Embed.Empty else "")
        + f"\n> {embed.description if embed.description != discord.Embed.Empty else ''}\n\n"
        + "\n\n".join(
            [
                f"**{field.name}**\n" + "> " + field.value.replace("\n", "\n> ")
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
            (" · " + embed.timestamp.strftime("%p %H:%M"))
            if embed.timestamp != discord.Embed.Empty
            else ""
        )
    )
