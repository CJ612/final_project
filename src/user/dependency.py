from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from user.crud import CRUDUser
from sqlalchemy.exc import NoResultFound


async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await CRUDUser.get(session, user_id)
        return user
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )