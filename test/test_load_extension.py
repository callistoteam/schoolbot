import os
import sys

from discord.ext.commands import Bot as Core

import schoolbot.bot as main

sys.path.append(os.path.abspath("schoolbot"))

def test_load():
    bot = Core("", help_command=None)
    failed = main.load_cogs(bot)
    assert len(failed) == 0
