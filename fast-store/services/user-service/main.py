from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from db import engine,get_session
from sqlmodel import SQLModel,Session
from models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok","service":"user-service"}

    