from fastapi import FastAPI,Depends,HTTPException
from contextlib import asynccontextmanager
from db import engine,get_session
from sqlmodel import SQLModel,Session, select
from shared.jwt_utils import verify_token
from auth import verify_password,create_access_token,hash_password
from models import User,UserPublic
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return {"status": "ok","service":"user-service"}

@app.post("/users/", response_model=UserPublic)
def create_user(user: User, session: Session = Depends(get_session)):
    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.post("/login")
def login(user_data: User, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    db_user = session.exec(statement).first()
   
    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
   
    token = create_access_token(data={"sub": str(db_user.id), "email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}