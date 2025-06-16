import asyncio
import logging
import sqlite3

import os

import asqlite
import twitchio
from twitchio.ext import commands
from twitchio import eventsub

from dotenv import load_dotenv


LOGGER: logging.Logger = logging.getLogger("Bot")
load_dotenv(".env")

# Assigns secret access token to "token".
CLIENT_ID: str = os.environ["CLIENT_ID"]  # timetogrow_ app
CLIENT_SECRET: str = os.environ["CLIENT_SECRET"]  # timetogrow_ app
# BOT_ID: str = os.environ["BOT_ID"]
# OWNER_ID: str = os.environ["OWNER_ID"]
BOT_ID: str = "930025545"
OWNER_ID: str = "501667269" #ambivalentbunnie


class Bot(commands.Bot):
    def __init__(self, *, token_database: asqlite.Pool) -> None:
        self.token_database = token_database
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
        )

    #Mysty - (ref notes in components.py)
    # When you call Bot.load_module("component") on L 43 in bot.py
    # It looks for a file named component.py
    # If it finds it and it loads it (basically imports it) and calls async def setup() injecting itself (the bot) into that function
    # So in setup you have access to the Bot which can be used to add your Component

    # URL to give bot permissions 
    # http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20channel:read:redemptions (This is wrong? remove redemptions?)
    # http://localhost:4343/oauth?scopes=channel:bot%20channel:read:redemptions
    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.load_module("component")

        # Subscribe to read chat (eve4nt_message) from our channel as the bot...
        # This creates and opens a websocket to Twitch EventSub...
        subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID)
        await self.subscribe_websocket(payload=subscription)

        # Subscribe and listen to when a stream goes live..
        # For this example listen to our own stream...
        subscription = eventsub.StreamOnlineSubscription(broadcaster_user_id=OWNER_ID)
        await self.subscribe_websocket(payload=subscription)

        #Subscribe and listen to channel points redemptions
        redeems_add = eventsub.ChannelPointsRedeemAddSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID)
        redeems_update  = eventsub.ChannelPointsRedeemUpdateSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID)
        await self.subscribe_websocket(payload=redeems_add)
        await self.subscribe_websocket(payload=redeems_update)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        # We don't need to call this manually, it is called in .login() from .start() internally...

        async with self.token_database.acquire() as connection:
            rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        # Create our token table, if it doesn't exist..
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)


def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, Bot(token_database=tdb) as bot:
            await bot.setup_database()
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()