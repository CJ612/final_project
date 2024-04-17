import asyncio
from fastapi import HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from user.dependency import get_correct_user_frontend
from database.models import User
from exception import RedirectException

async def get_user_or_redirect(request: Request, user: User | None = Depends(get_correct_user_frontend)) -> User:
    if not user:
        raise RedirectException(url="/")
    return user

def get_all_statistics(data) -> dict:
    all_data = {}
    
    all_data['data'] = []
    all_data['accuracy'] = []
    all_data['labels'] = []
    all_data['temp1'] = []
    all_data['temp2'] = []
    all_data['hum1'] = []
    all_data['hum2'] = []
    all_data['wind1'] = []
    all_data['wind2'] = []

    for row in data:
        atemperature = (
            0 if row.google_weather_temperature == row.measurement_temperature else 
            ((row.google_weather_temperature - row.measurement_temperature) / row.measurement_temperature) * 100 if row.measurement_temperature !=0 
            else (row.google_weather_temperature - row.measurement_temperature) * 100 
        )
        ahumidity = (0 if row.google_weather_humidity == row.measurement_humidity else 
                     ((row.google_weather_humidity - row.measurement_humidity) / row.measurement_humidity) * 100 if row.measurement_humidity !=0 else 
                     (row.google_weather_humidity - row.measurement_humidity) * 100 
        )
        awind = (0 if row.google_weather_wind == row.measurement_wind else 
                 ((row.google_weather_wind - row.measurement_wind) / row.measurement_wind) * 100 if row.measurement_wind !=0 else 
                 (row.google_weather_wind - row.measurement_wind) * 100
        )
        all_data['accuracy'].append({
            'date': row.measurement_date.date(),
            'atemperature': round(atemperature, ndigits=2), 
            'ahumidity': round(ahumidity, ndigits=2), 
            'awind': round(awind, ndigits=2)
            }) 
        all_data['labels'].append(str(row.measurement_date.date()))
        all_data['temp1'].append(row.google_weather_temperature)
        all_data['temp2'].append(row.measurement_temperature)
        all_data['hum1'].append(row.google_weather_humidity)
        all_data['hum2'].append(row.measurement_humidity)
        all_data['wind1'].append(row.google_weather_wind)
        all_data['wind2'].append(row.measurement_wind)
      
        all_data['data'].append(
            {
                'measurement_date': row.measurement_date.date(),
                'cities_city': row.cities_city,
                'cities_country': row.cities_country,
                'google_weather_description': row.google_weather_description,
                'google_weather_temperature': row.google_weather_temperature,
                'google_weather_humidity': row.google_weather_humidity,
                'google_weather_wind': row.google_weather_wind,
                'measurement_description': row.measurement_description,
                'measurement_temperature': row.measurement_temperature,
                'measurement_humidity': row.measurement_humidity,
                'measurement_wind': row.measurement_wind,
                'measurement_tool': row.measurement_tool
            }
        )

    return all_data

async def get_all_statistics_async(data):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, get_all_statistics, data)
    return await future

