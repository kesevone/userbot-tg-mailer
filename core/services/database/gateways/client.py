from typing import Optional, List

from sqlalchemy import select

from .base import BaseGateway
from ..models.general import ClientModel


class ClientGateway(BaseGateway):
    async def get(
        self, user_id: int
    ) -> Optional[ClientModel]:
        query = select(ClientModel).where(
            ClientModel.id == user_id
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def get_all(self) -> List[Optional[ClientModel]]:
        query = select(ClientModel)
        result = await self._session.execute(query)
        return result.scalars().unique().all()
