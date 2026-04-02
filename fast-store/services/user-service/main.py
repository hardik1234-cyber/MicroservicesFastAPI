from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from db import engine,get_session
from sqlmodel import SQLModel,Session
from models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the FastAPI application lifecycle using a context manager.
    
    The @asynccontextmanager decorator automatically handles startup and shutdown:
    - Code before yield: Runs when the app starts up
    - yield: Control passes to FastAPI, app begins serving requests
    - Code after yield: Runs when the app shuts down (guaranteed cleanup)
    
    This ensures database tables are created before the app handles any requests,
    and any cleanup code after yield will always execute when the app closes,
    even if an error occurs.
    """
    SQLModel.metadata.create_all(engine)
    yield
    

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok","service":"user-service"}

    