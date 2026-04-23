from fastapi import FastAPI
from app.routers import tasks
from app.database import engine
from app.models import Base
from app.routers import users
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is running"}