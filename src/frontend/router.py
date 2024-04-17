import asyncio
from fastapi import APIRouter, Request, Depends, status, HTTPException, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from weather_collecting.router import get_weather
from user.dependency import get_correct_user_frontend
from .dependency import get_user_or_redirect, get_all_statistics_async
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from tool.crud import CRUDTool
from weatherdescription.crud import CRUDWeatherDescription
from datetime import datetime, time
from measurement.crud import CRUDMeasurement
from googleweather.crud import CRUDGoogleWeather


router = APIRouter(
    prefix="", 
    tags=["frontend"]
)

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/auth")
async def get_login(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend), 
    not_auth: bool | None = None,
 ):
    if user:
        return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        if not_auth:
            request.session["message"] = "Authorization failed. Please, check your username or password."
    return templates.TemplateResponse("auth.html", {"request": request, "not_auth": not_auth})


@router.get("/logout", response_class=RedirectResponse)
async def get_logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/register")
async def get_register(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    if user:
        return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/")
async def get_index(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/404")
async def get_error(
    
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend), 
):
    return templates.TemplateResponse("404error.html", {"request": request, "user": user})

@router.get("/othererror")
async def get_error(
    
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend), 
):
    return templates.TemplateResponse("othererror.html", {"request": request, "user": user})

@router.get("/weatherinput")
async def get_weather_input(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend),
    session: AsyncSession = Depends(get_session),
):
    if user:
        data = {
            "tools": await CRUDTool.get_all_by_user_id(session, user.id),
            "weatherdescriptions": await CRUDWeatherDescription.get_all_weather_desctiptions(session),
            "uppertable": await get_weather(request, session, user),
        }
        
        return templates.TemplateResponse("weatherinput.html", {"request": request, "user": user, "data": data})
    return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/tools")
async def get_tools(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend),
    session: AsyncSession = Depends(get_session),
): 
    if user:
        data = await CRUDTool.get_all_by_user_id(session, user.id)
        return templates.TemplateResponse("tools.html", {"request": request, "user": user, "data": data})
    return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/profile")
async def get_profile(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend),
    session: AsyncSession = Depends(get_session),
):
    if user:
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.post("/tools")
async def add_tool(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    name: str = Form(...),
    description: str | None = Form(None),
    session: AsyncSession = Depends(get_session),
):
    tool = await CRUDTool.get_tool_by_toolname_and_userid(session, name, user.id)
    if tool:
        url = "/tools"
        request.session["message"] = "This tool has already been added"

    else:
        data = {"name": name, "description": description, "userid": user.id, "cityid": None}
        tool = await CRUDTool.create(session, data)
        request.session["message"] = "The tool was added successfully"
    return RedirectResponse(url="/tools", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.post("/weatherinput")
async def add_measurement(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    tool: int = Form(...),
    weatherdescription: int = Form(...),
    temperature: int|None = Form(None),
    humidity: int|None = Form(None),
    windspeed: int|None = Form(None),
    cityid: int = Form(...),
    date: datetime = Form(...),
    gdesc: int = Form(...),
    gtemp: int = Form(...),
    ghum: int = Form(...),
    gwind: int = Form(...),
    session: AsyncSession = Depends(get_session),
):
    # если нет, пишем в БД, если есть, обновляем запись
    date = datetime.combine(date, time()) 
    data = {
        "userid": user.id,
        "toolid": tool,
        "cityid": cityid,
        "descriptionid": weatherdescription,
        "date": date,
        "temperature": temperature,
        "humidity": humidity,
        "windspeed": windspeed,
    }
    measurement = await CRUDMeasurement.get_by_userid_and_date(session, user.id, date)
    if measurement is None:
        for value in data.values():
            if value is None:
               request.session["wmessage"] = "The measurement was not added, not all data was entered"
               return RedirectResponse(url="/weatherinput", status_code=status.HTTP_301_MOVED_PERMANENTLY) 
        new_measurement = await CRUDMeasurement.create(session, data) 
        request.session["message"] = "A new measurement has been successfully added"   
    else:
        new_data = {key: value for key, value in data.items() if value is not None}
        if new_data:
            updated_measurement = await CRUDMeasurement.update(session, measurement, new_data)
            request.session["message"] = "This measurement has been updated successfully"

    # пишем в базу соответствующий прогноз погоды
    weatherdata = {
       "cityid": cityid,
       "date": date,
       "temperature": gtemp, 
       "humidity": ghum,
       "wind": gwind,
       "descriptionid": gdesc,
    }
    googleweather = await CRUDGoogleWeather.get_all_by_city_id_date(
            session, 
            cityid, 
            date
        )
    if googleweather is None:
        new_googleweather = await CRUDGoogleWeather.create(session, weatherdata)
    else:
        updated_google_weather = await CRUDGoogleWeather.update(session, googleweather, weatherdata)
    
    return RedirectResponse(url="/weatherinput", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/report")
async def get_report(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend),
    session: AsyncSession = Depends(get_session),
):
    if user:
        data = await CRUDMeasurement.get_all_by_user(session, user.id)
        all_data = await get_all_statistics_async(data)
        return templates.TemplateResponse("report.html", {
            "request": request, 
            "user": user, 
            'data': all_data['data'],
            "accuracy": all_data['accuracy'],
            "json_data1": all_data['labels'],
            "json_data2": all_data['temp1'],
            "json_data3": all_data['temp2'],
            "json_data4": all_data['hum1'],
            "json_data5": all_data['hum2'],
            "json_data6": all_data['wind1'],
            "json_data7": all_data['wind2']
            })
    return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.post("/updatetool")
async def update_tool(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    id: str = Form(...),
    name: str = Form(...),
    description: str | None = Form(None),
    session: AsyncSession = Depends(get_session),
):
    tool = await CRUDTool.get_tool_by_toolid_and_userid(session, id, user.id)
    if tool:
        data = {
            "name": name,
            "description": description
        }
        updated_tool = await CRUDTool.update(session, tool, data)
        request.session["message"] = "This tool has been updated successfully"

    return RedirectResponse(url="/tools", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.post("/deletetool")
async def delete_tool(
    request: Request,
    name: str,
    user: User = Depends(get_user_or_redirect),
    session: AsyncSession = Depends(get_session),   
):
    tool = await CRUDTool.get_tool_by_toolname_and_userid(session, name, user.id)
    if tool:
        deleted_tool = await CRUDTool.delete(session, tool)
        request.session["message"] = "This tool was successfully removed"
    else:
        request.session["message"] = "This tool was not found"
    return RedirectResponse(url="/tools", status_code=status.HTTP_301_MOVED_PERMANENTLY)