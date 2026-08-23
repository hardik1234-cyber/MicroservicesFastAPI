from contextlib import asynccontextmanager
from typing import Annotated

from schemas import Token, UserCreate, UserRead
from db import get_session,engine
from auth import authenticate_user, create_user, get_user_by_email
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session
from utils import create_access_token
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    docs_url="/users/docs",
    redoc_url="/users/redoc",
    openapi_url="/users/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/register", response_model=UserRead)
async def register(
    user_in: UserCreate,
    session: Session = Depends(get_session),  # noqa: B008
):
    user = get_user_by_email(session=session, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = create_user(session=session, email=user_in.email, password=user_in.password)

    return user


@app.post("/users/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
