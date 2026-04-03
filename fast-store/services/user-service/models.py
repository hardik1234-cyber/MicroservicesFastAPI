from sqlmodel import SQLModel,Field
from typing import Optional


class User(SQLModel, table= True):
    """
    User model representing a user entity in the database.
    
    Attributes:
        id (Optional[int]): Primary key. Auto-generated if not provided.
        name (str): User's full name.
        email (str): User's email address.
        password (str): User's hashed password.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    password: str
    

class UserPublic(SQLModel):
    """
    Public user model for API responses.
    
    This model excludes sensitive information like passwords and is used
    when returning user data to clients. Only public-facing fields are included.
    
    Attributes:
        id (int): User's unique identifier.
        name (str): User's full name.
        email (str): User's email address.
    """
    id: int
    name: str
    email: str

    
    

