from sqlmodel import create_engine,Session

engine = create_engine("sqlite://database.db",connect_args={"check_same_thread":False})

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
        
        