from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")

engine = create_async_engine(
 CONNECTION_STRING,
 echo=True,
 future=True,
 pool_pre_ping=True,
 connect_args={"statement_cache_size": 0}
)

async_session_maker = async_sessionmaker(
 engine,
 class_=AsyncSession,
 expire_on_commit=False,
 autoflush=False,
 autocommit=False
)

database_context = declarative_base()

async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def initialize_database():
    print("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(database_context.metadata.create_all)

    print("Database initialized")