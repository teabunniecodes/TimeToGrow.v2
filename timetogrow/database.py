from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import asyncpg


class Database:
    def __init__(self, pool: asyncpg.Pool[asyncpg.Record]) -> None:
        self.pool = pool

    async def setup(self) -> None:
        async with self.pool.acquire() as connection:
            with open("database/SCHEMA.sql") as schema:
                await connection.execute(schema.read())

        print("Successfully setup database.")
        # logger.info("Successfully setup database.")

    # async def update_stats(
    #     self,
    #     username: str,
    #     /,
    #     *,
    #     minutes: int = 0,
    #     planted: int = 0,
    #     watered: int = 0,
    #     wilted: int = 0,
    #     killed: int = 0,
    #     epic: int = 0,
    #     sabotaged: int = 0,
    #     victim: int = 0,
    #     disasters: int = 0,
    #     survived: int = 0,
    #     thugged: int = 0,
    # ) -> None:
    #     query: str = """
    #     INSERT INTO stats(username) VALUES ($1) ON CONFLICT DO UPDATE SET
    #         minutes = minutes + $2,
    #         planted = planted + $3,
    #         watered = watered + $4,
    #         wilted = wilted + $5,
    #         killed = killed + $6,
    #         epic = epic + + $7,
    #         sabotaged = sabotaged + $8,
    #         victim = victim + $9,
    #         disasters = disasters + $10,
    #         survived = survived + $11,
    #         thugged = thugged + $12
    #     WHERE username = $1
    #     """

    #     async with self.pool.acquire() as connection:
    #         await connection.execute(
    #             query,
    #             username,
    #             minutes,
    #             planted,
    #             watered,
    #             wilted,
    #             killed,
    #             epic,
    #             sabotaged,
    #             victim,
    #             disasters,
    #             survived,
    #             thugged,
    #         )

    #     logger.info(f"Updated stats for {username}")
