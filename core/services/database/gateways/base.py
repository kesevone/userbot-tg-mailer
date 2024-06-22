from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from core.services.database.models.base import Base


class BaseGateway:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, *instances: "Base") -> None:
        self._session.add_all(instances)

    async def commit(self, *instances: "Base") -> None:
        if instances:
            self._session.add_all(instances)

        await self._session.commit()

    async def delete(self, *instances: Base) -> None:
        for instance in instances:
            await self._session.delete(instance)
