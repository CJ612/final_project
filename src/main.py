# git clone https://github.com/CJ612/final_project.git

# uvicorn main:app --reload

# pip freeze > requirements.txt

# http://localhost:8000/docs

# cd ./src

# 80 - http
# 443 - https
# 4441 - test
# 6379 - redis
# 5432 - psql

from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from config import SECRET_KEY
from database.database import create_all, drop_all
from user.router import router as user_router
from tool.router import router as tool_router
from measurement.router import router as measurement_router
from frontend.router import router as frontend_router
from weatherdescription.router import router as weather_description_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()
app.mount("/img", StaticFiles(directory="frontend/templates/img"), name="img")
app.mount("/css", StaticFiles(directory="frontend/templates/css"), name="css")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(user_router)
app.include_router(tool_router)
app.include_router(measurement_router)
app.include_router(frontend_router)
app.include_router(weather_description_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return RedirectResponse(url='/404')
    if exc.status_code == 500:
        return RedirectResponse(url='/othererror')
    else:
        return RedirectResponse(url='/')


# пересоздание таблиц БД
@app.get("/update_table")
async def update_table():
    await drop_all()
    await create_all()
    return 200
