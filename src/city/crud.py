from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import City


class CRUDCity:
    # города парсятся, пользователь не может добавить или удалить их
    # только выбрать в измерениях
    # при удалении пользователя удаляются и все города, где он измерял

    @staticmethod
    async def get(session: AsyncSession, city_id: int):
        city = select(City).filter(City.id == city_id)
        city = await session.execute(city)
        city = city.scalar_one()
        return city


    @staticmethod
    async def get_all(session: AsyncSession):
        cities = await session.execute(select(City))
        cities = cities.scalars().all()
        return cities

    @staticmethod
    async def create(session: AsyncSession, city_data: dict):
        city = City(**city_data)
        session.add(city)
        await session.commit()
        await session.refresh(city)
        return city

    @staticmethod
    async def delete(session: AsyncSession, city: City):
        await session.delete(city)
        await session.commit()

    @staticmethod
    async def get_city_by_cityname_country(session: AsyncSession, cityname: str, country: str):
        city = select(City).filter(City.name == cityname, City.country == country)
        city = await session.execute(city)
        city = city.scalar_one_or_none()
        if city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
            )
        return city
    
    @staticmethod
    async def get_city_by_user(session: AsyncSession, user_id: int):
        cities = select(City).filter(City.userid == user_id)
        cities = await session.execute(cities)
        cities = cities.scalars().all()
        if cities is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cities not found"
            )
        return cities