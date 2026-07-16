from datetime import datetime
from sqlmodel import Field, SQLModel


class User(SQLModel,table=True):
    username: str = Field(index=True, unique=True,primary_key=True)
    password: str
    email: str = Field(index=True, unique=True)

class UserLogin(SQLModel):
    username: str
    password:str

class UserSignUp(UserLogin):
    email: str

class Token(SQLModel):
    access_token: str
    token_type: str

class DataToken(SQLModel):
    username: str
