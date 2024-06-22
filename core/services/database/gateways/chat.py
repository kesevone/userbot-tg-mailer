from typing import Optional, List

from sqlalchemy import select

from .base import BaseGateway
from ..models.general import ChatModel


class ChatGateway(BaseGateway):
    async def get(self, chat_id: int) -> Optional[ChatModel]:
        query = select(ChatModel).where(
            ChatModel.id == chat_id
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def get_all(self, user_id: Optional[int] = None) -> List[Optional[ChatModel]]:
        query = select(ChatModel).where(
            (ChatModel.user_id == user_id) | (user_id is None)
        )
        result = await self._session.execute(query)
        return result.scalars().unique().all()
