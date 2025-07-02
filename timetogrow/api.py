import asyncio
import json
import logging
import secrets
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

import twitchio
from sse_starlette import EventSourceResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles


if TYPE_CHECKING:
    from .bot import Bot
else:
    from twitchio.ext.commands import Bot


logger: logging.Logger = logging.getLogger(__name__)


class DataEvent:
    event: str
    username: str


class DataPayload:
    extra: DataEvent | None
    # plants: list[PlantData]


class Server(twitchio.web.StarletteAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.bot: Bot | None = None
        self.add_route("/event", self.event_endpoint, methods=["GET"])
        self.mount("/", app=StaticFiles(directory="website", html=True), name="static")

        self.listeners: dict[str, asyncio.Queue[DataPayload]] = {}

    def dispatch(self, data: DataPayload) -> None:
        asyncio.create_task(self._dispatch(data=data))

    async def _dispatch(self, data: DataPayload) -> None:
        for queue in self.listeners.values():
            await queue.put(data)

    async def event_endpoint(self, request: Request) -> EventSourceResponse:
        identifier: str = secrets.token_urlsafe(12)
        self.listeners[identifier] = asyncio.Queue()

        return EventSourceResponse(self.process_event(identifier=identifier, request=request))

    async def process_event(self, *, identifier: str, request: Request) -> AsyncGenerator[str]:
        # logger.info(f'Event Listener "{identifier}" has connected.')
        queue: asyncio.Queue[DataPayload] = self.listeners[identifier]

        if self.bot:
            # yield json.dumps({"event": None, "plants": self.bot.plants_to_json()})
            print("test")
        while True:
            try:
                data: DataPayload = await queue.get()
                yield json.dumps(data)
            except asyncio.CancelledError:
                break

            if await request.is_disconnected():
                break

        # logger.info(f'Event Listener "{identifier}" has disconnected.')
        del self.listeners[identifier]
