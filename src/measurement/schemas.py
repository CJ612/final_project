from pydantic import BaseModel
from datetime import date
from typing import Optional

class MeasurementBase(BaseModel):
    userid: int
    toolid: int
    cityid: int
    descriptionid: int
    date: date
    temperature: int
    humidity: int
    windspeed: int

class MeasurementSelect(MeasurementBase):
    id: int

    class Config:
        from_attributes = True

class MeasurementUpdate(MeasurementBase):
    toolid: Optional[int]
    descriptionid: Optional[int]
    temperature: Optional[int]
    humidity: Optional[int]
    windspeed: Optional[int]