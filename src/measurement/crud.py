from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database.models import Measurement, GoogleWeather, City, WeatherDescription, Tool
# from database.models import WeatherDescription as wd2


class CRUDMeasurement:

    @staticmethod
    async def get(session: AsyncSession, measurement_id: int):
        measurement = select(Measurement).filter(Measurement.id == measurement_id)
        measurement = await session.execute(measurement)
        measurement = measurement.scalar_one()
        return measurement


    @staticmethod
    async def get_all(session: AsyncSession):
        measurements = await session.execute(select(Measurement))
        measurements = measurements.scalars().all()
        return measurements

    @staticmethod
    async def create(session: AsyncSession, measurement_data: dict):
        measurement = Measurement(**measurement_data)
        session.add(measurement)
        await session.commit()
        await session.refresh(measurement)
        return measurement

    @staticmethod
    async def update(session: AsyncSession, measurement: Measurement, measurement_data: dict):
        for key, value in measurement_data.items():
            setattr(measurement, key, value)
        await session.commit()
        await session.refresh(measurement)
        return measurement

    @staticmethod
    async def delete(session: AsyncSession, measurement: Measurement):
        await session.delete(measurement)
        await session.commit()

    @staticmethod
    async def get_all_by_user(session: AsyncSession, user_id: int):
        wd_alias1 = select(WeatherDescription).alias()
        wd_alias2 = select(WeatherDescription).alias()

        measurements = await session.execute(
            select(Measurement.cityid.label('measurement_cityid'), 
                    Measurement.date.label('measurement_date'),
                    Measurement.descriptionid.label('measurement_did'),
                    Measurement.temperature.label('measurement_temperature'),
                    Measurement.humidity.label('measurement_humidity'),
                    Measurement.windspeed.label('measurement_wind'),
                    GoogleWeather.descriptionid.label('google_weather_did'),
                    GoogleWeather.temperature.label('google_weather_temperature'),
                    GoogleWeather.humidity.label('google_weather_humidity'),
                    GoogleWeather.wind.label('google_weather_wind'),
                    City.name.label('cities_city'),
                    City.country.label('cities_country'),
                    wd_alias1.c.skydescription.label('measurement_description'),
                    wd_alias2.c.skydescription.label('google_weather_description'),
                    Tool.name.label('measurement_tool')
                    ).where(Measurement.cityid == GoogleWeather.cityid
                            ).where(Measurement.cityid == City.id
                                 ).where(Measurement.descriptionid == wd_alias1.c.id,  
                                         ).where(Measurement.toolid == Tool.id 
                                        #   ).where(GoogleWeather.descriptionid == wd2.id 
                                            ).where(GoogleWeather.descriptionid == wd_alias2.c.id 
                    ).filter(Measurement.userid == user_id)
        )
        return measurements
    
    @staticmethod
    async def get_all_by_period(session: AsyncSession, date_begin: datetime, date_end: datetime):
        measurements = await session.execute(select(Measurement).filter(Measurement.date >= date_begin, Measurement.date <= date_end))
        measurements = measurements.scalars().all()
        return measurements
    
    @staticmethod
    async def get_all_by_tool(session: AsyncSession, tool_id: int):
        measurements = await session.execute(select(Measurement).filter(Measurement.toolid == tool_id))
        measurements = measurements.scalars().all()
        return measurements
    
    @staticmethod
    async def get_by_userid_and_date(session: AsyncSession, user_id: int, date: datetime):
        measurement = select(Measurement).filter(Measurement.userid == user_id, Measurement.date == date)
        measurement = await session.execute(measurement)
        measurement = measurement.scalar_one_or_none()
        return measurement 

    @staticmethod
    async def get_measurements_by_user(session: AsyncSession, user_id: int):
        measurements = select(Measurement).filter(Measurement.userid == user_id)
        measurements = await session.execute(measurements)
        measurements = measurements.scalars().all()
        return measurements


 