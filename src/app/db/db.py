from typing import Any

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import settings

from .models import Base


def get_database_url() -> str:
    # return f"postgresql+asyncpg://{sdb.user}:{sdb.password}@{sdb.host}"
    return f"sqlite+aiosqlite:///{settings.database.path}"


def get_engine() -> AsyncEngine:
    print(get_database_url())
    print(get_database_url())
    print(get_database_url())
    print(get_database_url())
    return create_async_engine(
        get_database_url(),
        # echo=True,
    )


async def init_models() -> None:
    engine = get_engine()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


engine = get_engine()
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# add enforcement for foreign keys
@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_fks(dbapi_connection: Any, _: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
