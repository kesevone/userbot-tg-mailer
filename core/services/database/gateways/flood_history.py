from typing import Optional, List

from sqlalchemy import select

from .base import BaseGateway
from ..models.general import FloodHistoryModel


class FloodHistoryGateway(BaseGateway):
    async def get(self, pk: int) -> Optional[FloodHistoryModel]:
        query = select(FloodHistoryModel).where(
            FloodHistoryModel.id == pk,
        )

        result = await self._session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        user_id: Optional[int] = None,
        text: Optional[str] = None,
        settings: Optional[dict] = None,
        status: Optional[bool] = None,
    ) -> Optional[List[FloodHistoryModel]]:
        query = select(FloodHistoryModel).where(
            (FloodHistoryModel.user_id == user_id) | (user_id is None),
            (FloodHistoryModel.text == text) | (text is None),
            (FloodHistoryModel.settings == settings) | (settings is None),
            (FloodHistoryModel.status == status) | (status is None),
        )

        result = await self._session.execute(query)
        return result.scalars().unique().all()
