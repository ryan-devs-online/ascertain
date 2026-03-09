import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from db.base import Base

load_dotenv()
database_url = os.environ["DATABASE_URL"]
engine = create_async_engine(database_url, echo=True)


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
