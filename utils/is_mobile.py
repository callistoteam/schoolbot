import discord


def is_mobile(User):
    if not hasattr(User, "mobile_status"):
        return False

    if User.mobile_status == discord.Status.offline:
        return False

    return True
