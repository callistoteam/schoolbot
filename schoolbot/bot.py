def load_cogs(bot):
    extensions = [
        "schoolbot.cogs.events",
        "schoolbot.cogs.school",
        "schoolbot.cogs.general",
    ]
    failed_list = []

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            failed_list.append(extension)

    if failed_list:
        print(f"\nFailed to load extension. \n{''.join(failed_list)}")

    return failed_list
