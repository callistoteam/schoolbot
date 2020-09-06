import os
import sys

from discord.ext.commands import Bot

sys.path.append(os.path.abspath("./"))

import cogs


def test_load():
    assert len(cogs.load(Bot("", help_command=None))) == 0
