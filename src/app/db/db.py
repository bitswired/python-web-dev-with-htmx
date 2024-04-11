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
    """
    Get the URL for the database connection.

    Returns:
        str: The database URL.
    """
    return f"sqlite+aiosqlite:///{settings.database.path}"


def get_engine() -> AsyncEngine:
    """
    Get the asynchronous database engine.

    Returns:
        AsyncEngine: The asynchronous database engine.
    """
    print(get_database_url())
    print(get_database_url())
    print(get_database_url())
    print(get_database_url())
    return create_async_engine(
        get_database_url(),
        # echo=True,
    )


async def init_models() -> None:
    """
    Initialize the database models.

    Returns:
        None
    """
    engine = get_engine()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


engine = get_engine()
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_fks(dbapi_connection: Any, _: Any) -> None:
    """
    Enable foreign key constraints for a SQLite database connection.

    Args:
        dbapi_connection (Any): The SQLite database connection.
        _ (Any): Placeholder argument.

    Returns:
        None
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
