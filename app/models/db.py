from tortoise import Tortoise

from app.settings import db_name


async def run(generate_schemas=False):
    await Tortoise.init(
        db_url=f'sqlite://{db_name}',
        modules={'models': ['app.models.plot']}
    )

    if generate_schemas:
        await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()