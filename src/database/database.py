from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./database/db.db"

engine = create_async_engine(DATABASE_URL, echo=False)

Base = declarative_base()


async def get_session():

    async with sessionmaker(engine, class_=AsyncSession)() as session:

        yield session

async def create_all():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)