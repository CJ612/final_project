from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from weatherdescription.crud import CRUDWeatherDescription
from sqlalchemy.exc import NoResultFound


async def get_weatherdescription(weatherdescription_id: int, session: AsyncSession = Depends(get_session)):
    try:
        weatherdescription = await CRUDWeatherDescription.get(session, weatherdescription_id)
        return weatherdescription
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Weather Description not found"
        )