from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from database.database import get_session
from database.models import User
from user.schemas import UserCreate, UserInOut, UserBase, UserUpdate
from user.crud import CRUDUser
from user.auth import create_access_token, verify_password, hash_password
from .dependency import get_current_user, get_user_by_id
from city.crud import CRUDCity
from tool.crud import CRUDTool
from measurement.crud import CRUDMeasurement
from frontend.dependency import get_user_or_redirect


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDUser.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth")
async def login_for_access_token_frontend(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDUser.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        return RedirectResponse(url="/auth?not_auth=true", status_code=status.HTTP_303_SEE_OTHER)
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.post("/register")
async def register_user(
    username: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    password = hash_password(password)
    data = {
        "username": username, 
        "name": name,
        "age": age,
        "password": password, 
        "email": email}
    user = await CRUDUser.create(session, data)
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response

@router.post("/", response_model=UserInOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user.password = hash_password(user.password)
    new_user = await CRUDUser.create(session, user.model_dump())
    if new_user is None:
        raise HTTPException(
                status_code=400, detail="Unique field already exists."
            )
    return new_user


@router.get("/{user_id}", response_model=UserInOut)
async def get_user(
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user

@router.post("/updateuser")
async def update_user(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    session: AsyncSession = Depends(get_session),
    name: str|None = Form(None),
    newpassword: str|None = Form(None),
    age: int|None = Form(None),
    email: str|None = Form(None),
    oldpassword: str|None = Form(None),

):
    if user:
        user_data = {}
        if oldpassword and verify_password(oldpassword, user.password):
            if newpassword:
                password = hash_password(newpassword)
                user_data['password'] = password
            else:
                password = oldpassword

            if name:
                user_data['name'] = name
            if age:
                user_data['age'] = age
            if email:
                user_data['email'] = email

            updated_user = await CRUDUser.update(session, user, user_data)
            request.session["message"] = "The current user's data has been successfully updated."
        else:
            request.session["wmessage"] = "The password is incorrect or was not entered."
        return RedirectResponse(url="/profile", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    

@router.post("/deleteuser")
async def delete_user(
    user: User = Depends(get_user_or_redirect), 
    session: AsyncSession = Depends(get_session)
):
    # удалить все city, tool & measurements по этому пользователю
    deleted_data = await delete_users_data(user.id, session) 
    if deleted_data is None:   
        user = await CRUDUser.delete(session, user)
    return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)

async def delete_users_data(user_id, session):
    measurements = await CRUDMeasurement.get_measurements_by_user(session, user_id)
    for measurement in measurements:
        measurement = await CRUDMeasurement.delete(session, measurement)
    tools = await CRUDTool.get_all_by_user_id(session, user_id)
    for tool in tools:
        tool = await CRUDTool.delete(session, tool)
    cities = await CRUDCity.get_cities_by_user(session, user_id)
    for city in cities:
        city = await CRUDCity.delete(session, city)
    return