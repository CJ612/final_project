from pydantic import BaseModel

class WeatherDescriptionBase(BaseModel):
    skydescription: str