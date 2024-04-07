from fastapi import APIRouter, Request, Depends, status, HTTPException, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from user.dependency import get_correct_user_frontend
from .dependency import get_user_or_redirect
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from tool.crud import CRUDTool
from weatherdescription.crud import CRUDWeatherDescription


router = APIRouter(
    prefix="", 
    tags=["frontend"]
)

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/auth")
async def get_login(
    request: Request, user: User | None = Depends(get_correct_user_frontend), not_auth: bool | None = None,
 ):
    if user:
        return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    return templates.TemplateResponse(
        "auth.html", {"request": request, "not_auth": not_auth}
    )


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

@router.get("/weatherinput")
async def get_weather_input(
    request: Request, 
    user: User | None = Depends(get_correct_user_frontend),
    session: AsyncSession = Depends(get_session),
):
    if user:
        data = {
            "tools": await CRUDTool.get_all_by_user_id(session, user.id),
            "weatherdescriptions": await CRUDWeatherDescription.get_all_weather_desctiptions(session)
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

@router.get("/report")
async def get_report(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    if user:
        return templates.TemplateResponse("report.html", {"request": request, "user": user})
    return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/profile")
async def get_profile(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
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
    return RedirectResponse(url="/tools", status_code=status.HTTP_301_MOVED_PERMANENTLY)