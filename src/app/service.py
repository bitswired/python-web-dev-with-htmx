from dataclasses import dataclass
from typing import AsyncGenerator

import bcrypt
import litellm
from fastapi import HTTPException
from markdown import markdown
from sqlalchemy import ScalarResult, func, select
from sqlalchemy.orm import selectinload

from app import schemas
from app.db import AsyncSession, models

# @chatprompt(
#     SystemMessage("You are a movie buff."),
#     UserMessage("What is your favorite quote from Harry Potter?"),
#     AssistantMessage(
#         Quote(
#             quote="It does not do to dwell on dreams and forget to live.",
#             character="Albus Dumbledore",
#         )
#     ),
#     UserMessage("What is your favorite quote from {movie}?"),
# )
# def get_movie_quote(movie: str) -> Quote: ...


# get_movie_quote("Iron Man")
# # Quote(quote='I am Iron Man.', character='Tony Stark')


@dataclass
class AppService:
    session: AsyncSession

    async def get(self) -> ScalarResult[models.User]:
        session = self.session
        async with session.begin():
            result: ScalarResult[models.User] = await self.session.scalars(
                select(models.User).limit(20)
            )
        return result

    async def create_user(self, data: schemas.Signup) -> models.User:
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

        user = models.User(
            username=data.username, hashed_password=hashed_password.decode()
        )

        async with self.session.begin():
            self.session.add(user)
        return user

    async def login(self, daat: schemas.Login) -> models.User:
        user = await self.session.scalar(
            select(models.User).where(models.User.username == daat.username)
        )

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if not bcrypt.checkpw(daat.password.encode(), user.hashed_password.encode()):
            raise HTTPException(status_code=400, detail="Invalid password")

        return user

    async def get_user_by_id(self, id: int) -> models.User:
        async with self.session.begin():
            user = await self.session.scalar(
                select(models.User).where(models.User.id == id)
            )

        return user

    async def get_all_chats(self, user: models.User) -> ScalarResult[models.Chat]:
        session = self.session
        async with session.begin():
            subquery = (
                select(
                    models.ChatMessage.chat_id,
                    func.max(models.ChatMessage.create_date).label("max_date"),
                )
                .where(models.ChatMessage.chat_id == models.Chat.id)
                .group_by(models.ChatMessage.chat_id)
                .alias()
            )
            chats = await self.session.scalars(
                select(models.Chat)
                .where(models.Chat.user_id == user.id)
                .join(subquery, models.Chat.id == subquery.c.chat_id)
                .order_by(subquery.c.max_date.desc())
                .options(selectinload(models.Chat.messages))
            )

        return chats

    # async def get_chats(self, user: models.User) -> list[models.Chat]:
    #     async with self.session.begin():
    #         chats = await self.session.scalars(
    #             select(models.Chat)
    #             .where(models.Chat.user_id == user.id)
    #             .options(selectinload(models.Chat.messages))
    #         )
    #     return chats

    async def get_chat_by_id(self, chat_id: int, user: models.User) -> models.Chat:
        async with self.session.begin():
            chat = await self.session.scalar(
                select(models.Chat)
                .where(models.Chat.id == chat_id and models.Chat.user_id == user.id)
                .options(selectinload(models.Chat.messages))
            )
        return chat

    async def create_chat(
        self, user: models.User, data: schemas.CreateChat
    ) -> models.Chat:
        chat = models.Chat(name=data.message, user_id=user.id)

        message = models.ChatMessage(kind="human", content=data.message)

        chat.messages.append(message)

        async with self.session.begin():
            self.session.add(chat)
        return chat

    async def add_message(
        self, user: models.User, data: schemas.AddMessage, chat_id: int
    ) -> models.ChatMessage:
        async with self.session.begin():
            chat = await self.session.scalar(
                select(models.Chat).where(models.Chat.id == chat_id)
            )

            if chat is None:
                raise HTTPException(status_code=404, detail="Chat not found")

            message = models.ChatMessage(
                kind="human", content=data.message, chat_id=chat.id
            )

            self.session.add(message)
        return message

    async def generate(self, chat_id: int) -> AsyncGenerator[dict, None]:
        async with self.session.begin():
            chat = await self.session.scalar(
                select(models.Chat)
                .where(models.Chat.id == chat_id)
                .options(
                    selectinload(models.Chat.messages),
                )
            )

        messages: list[dict] = []

        for message in chat.messages:
            if message.kind == "human":
                messages.append({"role": "user", "content": message.content})
            else:
                messages.append({"role": "assistant", "content": message.content})

        response = await litellm.acompletion(
            model="gpt-3.5-turbo", messages=messages, stream=True
        )

        res = ""
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                res += content
                s = f"""
                <div id="ai-sse" class="prose prose-sm w-full flex flex-col [&>*]:flex-grow">
                    {markdown(res, extensions=["fenced_code"])}
                </div>
                """
                yield {"event": "message", "id": "id", "data": s}

        async with self.session.begin():
            gen_message = models.ChatMessage(
                kind="assistant", content=res, chat_id=chat.id
            )
            self.session.add(gen_message)

        s = f"""
        <div class="prose prose-sm w-full flex flex-col [&>*]:flex-grow">
            {markdown(res, extensions=["fenced_code"])}
        </div>

        <div id="stream" hx-swap-oob="true" hx-swap="outerHTML"></div>
        """
        yield {"event": "message", "id": "id", "data": s}
