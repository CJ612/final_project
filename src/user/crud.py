from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


class CRUDUser:

    @staticmethod
    async def get(session: AsyncSession, user_id: int):
        user = select(User).filter(User.id == user_id)
        user = await session.execute(user)
        user = user.scalar_one()
        return user


    @staticmethod
    async def get_all(session: AsyncSession):
        users = await session.execute(select(User))
        users = users.scalars().all()
        return users

    @staticmethod
    async def create(session: AsyncSession, user_data: dict):
        user = User(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update(session: AsyncSession, user: User, user_data: dict):
        for key, value in user_data.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user: User):
        await session.delete(user)
        await session.commit()


    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str):
        query = select(User).filter(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
    
        return user