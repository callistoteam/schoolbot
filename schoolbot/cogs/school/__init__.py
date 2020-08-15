import os

from .meal import Meal
from .academic_calendar import AcademicSchedule


def setup(bot):
    bot.add_cog(Meal(bot, os.environ["API_KEY"]))
    bot.add_cog(AcademicSchedule(bot, os.environ["API_KEY"]))
