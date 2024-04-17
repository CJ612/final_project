import aiohttp
import asyncio
from datetime import datetime, time
from fastapi import Request, APIRouter
from database.models import User
from city.crud import CRUDCity
from weatherdescription.crud import CRUDWeatherDescription
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request as Rquest
from sqlalchemy.ext.asyncio import AsyncSession
from weatherdescription.crud import CRUDWeatherDescription
from datetime import datetime, time


router = APIRouter(
    prefix="/winput", 
    tags=["winput"]
)
        
async def get_google_weather(userid: int, request: Rquest = None) -> dict:
    api_key = 'de5b400704cc4fc8b16191150240904'
    # ip_address = request.client.host
    ip_address = '87.210.159.222'
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.weatherapi.com/v1/current.json?q={ip_address}&lang=en&key={api_key}") as response:
            data = await response.json()
            if data:
                date = datetime.now().date()
                city = data['location']['name']
                country = data['location']['country']
                sky_description = data['current']['condition']['text']
                         
                temperature = data['current']['temp_c']
                humidity = data['current']['humidity']
                wind = data['current']['wind_kph']
                current_weather = {
                    'date': date,
                    'temperature': int(temperature),
                    'humidity': int(humidity),
                    'wind': int(wind)
                }
                return {
                    'weather': current_weather, 
                    'city': city, 
                    'country': country,
                    'description': sky_description
                }
            
async def get_weather(
    request: Request,
    session: AsyncSession, 
    user: User ,       
):
    weatherdata = await get_google_weather(session, user.id)
    # определяем id или добавляем
    if weatherdata:
        sky_description = weatherdata['description']
        date = datetime.combine(weatherdata['weather']['date'], time()) 
        description = await CRUDWeatherDescription.get_weather_desctiption_by_name(session, sky_description)
        if description:
            descriptionid = description.id
        else:
            descerdata = {'skydescription': sky_description}
            newdescription = await CRUDWeatherDescription.create(session, descerdata)
            descriptionid = newdescription.id
        databasecity = await CRUDCity.get_city_by_user_and_date(session, user.id, date)
        if databasecity:
            cityid = databasecity.id 
        else:
            citydata = {'name': weatherdata['city'], 'country': weatherdata['country'], 'userid': user.id, 'date': date} 
            newcity = await CRUDCity.create(session, citydata)
            cityid = newcity.id  
        weatherdata['weather']['descriptionid'] = descriptionid 
        weatherdata['weather']['cityid'] = cityid
               
    return weatherdata
