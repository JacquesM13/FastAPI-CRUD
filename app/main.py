from fastapi import FastAPI
from app.routers import tasks
from app.database import engine
from app.models import Base
from app.routers import users
import logging
from app.middleware.logging import log_requests

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.middleware("http")(log_requests)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is running here: http://127.0.0.1:8000/docs#/"}