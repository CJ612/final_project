# git clone https://github.com/CJ612/final_project.git

# uvicorn main:app --reload

# pip freeze > requirements.txt

# http://localhost:8000/docs

from fastapi import FastAPI

from database.database import create_all, drop_all
from user.router import router as user_router
from tool.router import router as tool_router
from measurement.router import router as measurement_router


app = FastAPI()

app.include_router(user_router)
app.include_router(tool_router)
app.include_router(measurement_router)

# пересоздание таблиц БД
@app.get("/update_table")
async def update_table():
    await drop_all()
    await create_all()
    return 200

