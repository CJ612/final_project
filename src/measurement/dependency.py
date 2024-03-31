from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from measurement.crud import CRUDMeasurement
from sqlalchemy.exc import NoResultFound


async def get_measurement(measurement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        measurement = await CRUDMeasurement.get(session, measurement_id)
        return measurement
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mesurement not found"
        )