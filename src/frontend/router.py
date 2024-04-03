from fastapi import APIRouter, Request, Depends, status, HTTPException 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from user.dependency import get_correct_user_frontend
from database.models import User


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