from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel,EmailStr

app = FastAPI()

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    
users_db = {}

@app.post('/signup')
def create_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user already exists")
    users_db[user.username] = user
    return {"message": "User Created"}

@app.post('/login')
def login(user: User):
    if user.username not in users_db or users_db[user.username].password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return {"message": "Login successful"}