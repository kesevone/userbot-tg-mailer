import asyncio
from types import TracebackType
from typing import Optional, Tuple, Type

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.services.database.gateways.general import Gateway


class SQLSessionContext:
    _session_pool: async_sessionmaker[AsyncSession]
    _session: Optional[AsyncSession]

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        self._session_pool = session_pool
        self._session = None

    async def __aenter__(self) -> Gateway:
        self._session: AsyncSession = await self._session_pool().__aenter__()
        return Gateway(session=self._session)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._session is None:
            return
        task: asyncio.Task = asyncio.create_task(self._session.close())
        await asyncio.shield(task)
        self._session = None