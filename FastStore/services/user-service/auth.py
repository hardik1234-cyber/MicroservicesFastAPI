from models import UserInDB
from passlib.context import CryptContext
from sqlmodel import Session, select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(session: Session, email: str):
    return session.exec(select(UserInDB).where(UserInDB.email == email)).first()


def create_user(session: Session, email: str, password: str):
    hashed_password = hash_password(password=password)
    user = UserInDB(email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session=session, email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user