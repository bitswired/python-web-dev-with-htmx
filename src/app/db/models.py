from __future__ import annotations

from datetime import datetime

from markdown import markdown
from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all models.
    Provides common attributes like create_date and update_date.
    """

    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    """
    Represents a user in the system.
    """

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uix_username"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    chats: Mapped[list[Chat]] = relationship(back_populates="user")


class Chat(Base):
    """
    Represents a chat in the system.
    """

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="chats")

    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    """
    Represents a message in a chat.
    """

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    chat: Mapped[Chat] = relationship(back_populates="messages")

    kind: Mapped[str] = mapped_column(nullable=False)

    content: Mapped[str] = mapped_column(nullable=False)

    @property
    def rendered_content(self) -> str:
        """
        Renders the content of the message as HTML using Markdown.
        """
        res: str = markdown(self.content, extensions=["fenced_code"])
        return res
