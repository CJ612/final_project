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