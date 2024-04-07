from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from weatherdescription.dependency import get_weatherdescription
from database.database import get_session
from database.models import WeatherDescription, User
from weatherdescription.schemas import WeatherDescriptionBase
from weatherdescription.crud import CRUDWeatherDescription
from user.router import get_current_user



router = APIRouter(
    prefix="/weatherdescription",
    tags=["weatherdescription"],
)

@router.get("/{weatherdescription_id}", response_model=WeatherDescriptionBase)
async def read_weatherdescription(weatherdescription: WeatherDescription = Depends(get_weatherdescription), user: User = Depends(get_current_user)):
    return weatherdescription

@router.post("/", response_model=WeatherDescriptionBase)
async def create_weatherdescription(weatherdescription: WeatherDescriptionBase, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    weatherdescription = await CRUDWeatherDescription.create(session, weatherdescription.dict())
    return weatherdescription

@router.delete("/{weatherdescription_id}")
async def delete_weatherdescription(
    weatherdescription: WeatherDescription = Depends(get_weatherdescription), session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user),
):
    weatherdescription = await CRUDWeatherDescription.delete(session, weatherdescription)
    return status.HTTP_204_NO_CONTENT