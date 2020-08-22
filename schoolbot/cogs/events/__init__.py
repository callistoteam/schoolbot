from .ready import Ready
from .error import Error


def setup(bot):
    bot.add_cog(Ready(bot))
    bot.add_cog(Error(bot))
