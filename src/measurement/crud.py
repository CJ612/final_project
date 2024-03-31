from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from database.models import Measurement


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
        measurements = await session.execute(select(Measurement).filter(Measurement.userid == user_id))
        measurements = measurements.scalars().all()
        return measurements
    
    @staticmethod
    async def get_all_by_period(session: AsyncSession, date_begin: date, date_end: date):
        measurements = await session.execute(select(Measurement).filter(Measurement.date >= date_begin, Measurement.date <= date_end))
        measurements = measurements.scalars().all()
        return measurements
    
    @staticmethod
    async def get_all_by_tool(session: AsyncSession, tool_id: int):
        measurements = await session.execute(select(Measurement).filter(Measurement.toolid == tool_id))
        measurements = measurements.scalars().all()
        return measurements


 