from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import GoogleWeather


class CRUDGoogleWeather:

    @staticmethod
    async def get(session: AsyncSession, google_weather_id: int):
        google_weather = select(GoogleWeather).filter(GoogleWeather.id == google_weather_id)
        google_weather = await session.execute(google_weather)
        google_weather = google_weather.scalar_one()
        return google_weather
    
    @staticmethod
    async def get_all_by_city_id_date(session: AsyncSession, city_id: int, date: datetime):
        google_weather = await session.execute(select(GoogleWeather).filter(GoogleWeather.cityid == city_id, GoogleWeather.date == date))
        google_weather = google_weather.scalar_one_or_none()
        return google_weather

    @staticmethod
    async def create(session: AsyncSession, google_weather_data: dict):
        google_weather = GoogleWeather(**google_weather_data)
        session.add(google_weather)
        await session.commit()
        await session.refresh(google_weather)
        return google_weather
        
    @staticmethod
    async def update(session: AsyncSession, googleweather: GoogleWeather, google_weather_data: dict):
        for key, value in google_weather_data.items():
            setattr(googleweather, key, value)
        await session.commit()
        await session.refresh(googleweather)
        return googleweather