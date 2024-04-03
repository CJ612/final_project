from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from user.crud import CRUDUser
from fastapi.security import OAuth2PasswordBearer
from fastapi.requests import Request
from .auth import verify_token, verify_token_not_exception
from .crud import CRUDUser
from .exceptions import exception_user_not_found, exception_auth


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/token",
    auto_error=False,
)

async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    if not token:
        raise exception_auth
    username = verify_token(token, exception_auth)
    user = await CRUDUser.get_user_by_username(session, username)
    if user is None:
        raise exception_user_not_found
    return user


async def get_token_cookie(request: Request):
    return request.cookies.get("access_token")


async def get_correct_user_frontend(
    token: str | None = Depends(get_token_cookie),
    session: AsyncSession = Depends(get_session),
):
    if token:
        username = verify_token_not_exception(token)
        if username:
            user = await CRUDUser.get_user_by_username(session, username)
            return user


async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await CRUDUser.get_by_id(session, user_id)
    if user is None:
        raise exception_user_not_found
    return user
