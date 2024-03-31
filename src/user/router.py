from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import User
from user.schemas import UserCreate, UserInOut, UserBase
from user.crud import CRUDUser
from user.dependency import get_user
from user.auth import verify_token, create_access_token, verify_password, hash_password
from city.crud import CRUDCity
from tool.crud import CRUDTool
from measurement.crud import CRUDMeasurement


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_name = verify_token(token, credentials_exception)
    user = await CRUDUser.get_user_by_username(session, user_name)
    if user is None:
        raise credentials_exception
    return user

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


@router.post("/me", response_model=UserInOut)
async def read_users_me(user: User = Depends(get_current_user)):
    return user


@router.get("/", response_model=list[UserBase])
async def read_users(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await CRUDUser.get_all(session)


@router.get("/{user_id}", response_model=UserInOut)
async def read_user(user: User = Depends(get_current_user)):
    return user

@router.post("/", response_model=UserInOut)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user.password = hash_password(user.password)
    user = await CRUDUser.create(session, user.dict())
    return user


@router.put("/{user_id}", response_model=UserInOut)
async def update_user(
    user_create: UserCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDUser.update(session, user, user_create.dict())
    return user


@router.delete("/{user_id}")
async def delete_user(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    # удалить все city, tool & measurements по этому пользователю
    measurements = await CRUDMeasurement.get_all_by_user(session, user.id)
    for measurement in measurements:
        measurement = await CRUDMeasurement.delete(session, measurement)
    tools = await CRUDTool.get_all_by_user_id(session, user.id)
    for tool in tools:
        tool = await CRUDTool.delete(session, tool)
    cities = await CRUDCity.get_city_by_user(session, user.id)
    for city in cities:
        city = await CRUDTool.delete(session, city)
    
    user = await CRUDUser.delete(session, user)
    return status.HTTP_204_NO_CONTENT