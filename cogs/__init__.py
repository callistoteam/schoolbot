import logging
import os
import re
import traceback

log = logging.getLogger("schoolbot.cogs")

Directory = os.path.dirname(os.path.realpath(__file__))


def load(Bot):
    Failed = []

    for Extension in [
        "cogs." + re.sub(".py", "", File)
        for File in os.listdir(Directory)
        if not "__" in File
    ]:
        try:
            Bot.load_extension(Extension)
        except:
            log.error(f"while loading extension {Extension}, an error occured.")
            traceback.print_exc()
            Failed.append(Extension)

    return Failed
