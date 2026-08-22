# from crud.users import get_user_by_email
import os

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # type: ignore
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict):
    data_to_encode = data.copy()
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)  # type: ignore
    return encoded_jwt