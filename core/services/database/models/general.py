from __future__ import annotations

from typing import Any, Optional, Self

from sqlalchemy import JSON
from sqlalchemy.orm import mapped_column, Mapped

from core.services.database.models.base import Base


class ClientModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    settings: Mapped[dict] = mapped_column(JSON)
    fullname: Mapped[str]

    @classmethod
    def create(cls, user_id: int, settings: dict, fullname: str) -> Self:
        return cls(id=user_id, settings=settings, fullname=fullname)

    def update_fullname(self, fullname: str) -> None:
        self.fullname = fullname

    def update_settings(self, settings: dict) -> None:
        self.settings = settings


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    name: Mapped[Optional[str]]

    @classmethod
    def create(cls, chat_id: int, user_id: int, name: Optional[str] = None) -> Self:
        return cls(id=chat_id, user_id=user_id, name=name)


class FloodHistoryModel(Base):
    __tablename__ = "flood_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    photo_id: Mapped[Optional[int]]
    text: Mapped[Optional[str]]
    settings: Mapped[dict] = mapped_column(JSON)
    status: Mapped[Optional[bool]]

    @classmethod
    def create(
        cls,
        user_id: int,
        settings: dict[str, Any],
        photo_id: Optional[str] = None,
        text: Optional[str] = None,
        status: Optional[bool] = None,
    ) -> Self:
        return cls(
            user_id=user_id,
            photo_id=photo_id,
            text=text,
            settings=settings,
            status=status,
        )

    def update_status(self, status: bool) -> None:
        self.status = status
