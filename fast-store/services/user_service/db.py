from sqlmodel import create_engine,Session
import os

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///database.db")

# check_same_thread is only for SQLite, not for PostgreSQL
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def get_session():
    """
    Dependency injection function that yields a database session.
    
    Used with FastAPI's Depends() to automatically provide a database session
    to route handlers. The session is automatically closed after each request.
    
    Yields:
        Session: A SQLModel database session for database operations.
    """
    with Session(engine) as session:
        yield session
        
        