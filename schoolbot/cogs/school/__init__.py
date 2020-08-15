import os

from .meal import Meal
from .academic_calendar import AcademicCalendar


def setup(bot):
    bot.add_cog(Meal(bot, os.environ["API_KEY"]))
    bot.add_cog(AcademicCalendar(bot, os.environ["API_KEY"]))
