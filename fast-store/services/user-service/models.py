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
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    email: str
    password: str
    
    

