from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import WeatherDescription


class CRUDWeatherDescription:

    @staticmethod
    async def get(session: AsyncSession, weather_description_id: int):
        weather_description = select(WeatherDescription).filter(WeatherDescription.id == weather_description_id)
        weather_description = await session.execute(weather_description)
        weather_description = weather_description.scalar_one()
        return weather_description

    @staticmethod
    async def create(session: AsyncSession, weather_description_data: dict):
        weather_description = WeatherDescription(**weather_description_data)
        session.add(weather_description)
        await session.commit()
        await session.refresh(weather_description)
        return weather_description

    @staticmethod
    async def get_weather_desctiption_by_name(session: AsyncSession, weather_description_name: str):
        weather_description = select(WeatherDescription).filter(WeatherDescription.skydescription == weather_description_name)
        weather_description = await session.execute(weather_description)
        weather_description = weather_description.scalar_one_or_none()
        # if weather_description is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail="Weather description not found"
        #     )
        return weather_description
    
    @staticmethod
    async def get_all_weather_desctiptions(session: AsyncSession):
        weather_description = select(WeatherDescription)
        weather_description = await session.execute(weather_description)
        weather_description = weather_description.scalars().all()
        
        return weather_description