import os
from .help import Help
from .search import Search
from .setting import Setting


def setup(bot):
    bot.add_cog(Help(bot))
    bot.add_cog(Search(bot, os.environ["API_KEY"]))
    bot.add_cog(Setting(bot))
