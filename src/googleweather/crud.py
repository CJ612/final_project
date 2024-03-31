from datetime import date
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
    async def get_all_by_city_id_date(session: AsyncSession, city_id: int, date: date):
        google_weather = await session.execute(select(GoogleWeather).filter(GoogleWeather.cityid == city_id, GoogleWeather.date == date))
        google_weather = google_weather.scalars().all()
        return google_weather

    @staticmethod
    async def create(session: AsyncSession, google_weather_data: dict):
        google_weather = GoogleWeather(**google_weather_data)
        session.add(google_weather)
        await session.commit()
        await session.refresh(google_weather)
        return google_weather