from fastapi import FastAPI,Depends,HTTPException,status
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from db import engine,get_session
from sqlmodel import SQLModel,Session, select
from utils import verify_pass,hash_pass
from oauth2 import create_access_token
from models import User,UserSignUp,Token,UserLogin
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



@app.post('/signup',status_code=status.HTTP_201_CREATED)
def sign_up(user: UserSignUp, db: Session = Depends(get_session)):

    existing_user = db.exec(select(User).where(User.username == user.username)).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    print(user)
    print(user.password)
    print(len(user.password))
    new_user = User(username=user.username,password=hash_pass(user.password),email=user.email)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Unable to add user , try again")
    finally:
        db.close()
    return "User Registered"

@app.post('/login',response_model=Token)
def login(user_creds: UserLogin,db: Session = Depends(get_session)):
    
    user = db.exec(select(User).where(User.username == user_creds.username)).one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials!"
        )

    if not verify_pass(user_creds.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials!"
        )
    
    try:
        access_token = create_access_token(data={"username": user.username})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Unable to login this user")
    finally:
        db.close()
    return Token(access_token=access_token,token_type="bearer")
            
