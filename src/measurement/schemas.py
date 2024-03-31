from pydantic import BaseModel
from datetime import date

class MeasurementBase(BaseModel):
    userid: int
    toolid: int|None
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