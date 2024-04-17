from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import Measurement, User
from measurement.schemas import MeasurementBase, MeasurementSelect
from measurement.crud import CRUDMeasurement
from measurement.dependency import get_measurement
from user.router import get_current_user

router = APIRouter(
    prefix="/measurement",
    tags=["measurement"],
)

@router.get("/{measurement_id}", response_model=MeasurementSelect)
async def read_measurement(measurement: Measurement = Depends(get_measurement), user: User = Depends(get_current_user)):
    return measurement

@router.post("/", response_model=MeasurementBase)
async def create_measurement(measurement: MeasurementBase, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    measurement = await CRUDMeasurement.create(session, measurement.dict())
    return measurement


@router.put("/{measurement_id}", response_model=MeasurementSelect)
async def update_measurement(
    measurement_create: MeasurementBase,
    measurement: Measurement = Depends(get_measurement),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    measurement = await CRUDMeasurement.update(session, measurement, measurement_create.dict())
    return measurement


@router.delete("/{measurement_id}")
async def delete_measurement(
    measurement: Measurement = Depends(get_measurement), 
    session: AsyncSession = Depends(get_session), 
    user: User = Depends(get_current_user),
):
    measurement = await CRUDMeasurement.delete(session, measurement)
    return status.HTTP_204_NO_CONTENT