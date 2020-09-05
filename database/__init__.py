from tortoise import Tortoise
from .models import *


async def init():
    await Tortoise.init(
        db_url="mysql://root:asdf@localhost:3306/test",
        modules={"models": ["database.models"]},
    )

    await Tortoise.generate_schemas(safe=True)