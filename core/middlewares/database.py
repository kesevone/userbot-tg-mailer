from multiprocessing.connection import Client
from typing import Any

from pyrogram_patch.middlewares.middleware_types import OnUpdateMiddleware
from pyrogram_patch.patch_helper import PatchHelper
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession

from core.services.database.context import SQLSessionContext


class DBSessionMiddleware(OnUpdateMiddleware):
    """
    A middleware class that provides a database session to the request handlers.

    Args:
        engine (AsyncEngine): The SQLAlchemy engine instance.
        session_pool (async_sessionmaker[AsyncSession]): The SQLAlchemy session pool.
    """

    def __init__(
        self, engine: AsyncEngine, session_pool: async_sessionmaker[AsyncSession]
    ) -> None:
        self.engine = engine
        self.session_pool = session_pool

    async def __call__(self, update: Any, client: Client, patch: PatchHelper):

        async with SQLSessionContext(session_pool=self.session_pool) as gw:
            patch.data["engine"] = self.engine
            patch.data["session_pool"] = self.session_pool
            patch.data["gateway"] = gw
