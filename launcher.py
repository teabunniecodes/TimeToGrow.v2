import asyncio

import asyncpg
import twitchio
# import uvicorn

import timetogrow


async def main() -> None:
    twitchio.utils.setup_logging()
    async with asyncpg.create_pool(
        user="bunnie", password="bunnie1!", database="timetogrow", host="localhost", port=5432
    ) as pool:
        # Now `pool` is an async connection pool for PostgreSQL
        # Example of using the pool to run queries asynchronously
        # async with pool.acquire() as connection:
        #     # Let's say you want to fetch data using the connection
        database: timetogrow.Database = timetogrow.Database(pool)
        await database.setup()
        # result = await connection.fetch("SELECT * FROM ")

        app: timetogrow.Server = timetogrow.Server()
        async with timetogrow.Bot(server=app, pool=pool, database=database) as bot:
            await bot.start()

        # app.bot = bot

        # config: uvicorn.Config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        # server: uvicorn.Server = uvicorn.Server(config)

        # # asyncio.create_task(bot.start())
        # await server.serve()


asyncio.run(main())
