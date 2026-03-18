from fastapi import FastAPI
from app.routers import tasks
from app.database import engine
from app.models import Base


app = FastAPI()

app.include_router(tasks.router)

