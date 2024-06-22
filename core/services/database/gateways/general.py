from sqlalchemy.ext.asyncio import AsyncSession

from core.services.database.gateways.base import BaseGateway
from core.services.database.gateways.chat import ChatGateway
from core.services.database.gateways.client import ClientGateway
from core.services.database.gateways.flood_history import FloodHistoryGateway


class Gateway(BaseGateway):
    flood_history: FloodHistoryGateway
    client: ClientGateway
    chat: ChatGateway

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.flood_history = FloodHistoryGateway(session=session)
        self.client = ClientGateway(session=session)
        self.chat = ChatGateway(session=session)
