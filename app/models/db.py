from tortoise import Tortoise


async def run(generate_schemas=False):
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models.plot']}
    )

    if generate_schemas:
        await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()