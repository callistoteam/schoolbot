import os

from .meal import Meal
from .academic_schedule import AcademicSchedule
from .article import Article
from .timetable import TimeTable


def setup(bot):
    bot.add_cog(Meal(bot, os.environ["API_KEY"]))
    bot.add_cog(AcademicSchedule(bot, os.environ["API_KEY"]))
    bot.add_cog(Article(bot))
    bot.add_cog(TimeTable(bot))
