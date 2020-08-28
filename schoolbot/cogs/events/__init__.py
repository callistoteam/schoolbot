from .ready import Ready


def setup(bot):
    bot.add_cog(Ready(bot))
