from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
from db import engine,get_session
from sqlmodel import SQLModel,Session, select
from models import User,UserPublic
import grpc
import product_pb2
import product_pb2_grpc

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

@app.get("/health")
def health_check():
    return {"status": "ok","service":"user-service"}

@app.post("/users/",response_model=UserPublic)
def create_user(user: User,db: Session = Depends(get_session)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/")
def read_users(db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users

@app.get("/users/{user_id}/purchases/{product_id}")
def get_user_purchase(
    user_id: int, 
    product_id: int,
    ):
 

    with grpc.insecure_channel("product-service:50051") as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)

        response = stub.GetProduct(product_pb2.ProductRequest(id=product_id))
    
    return {
        "user_id": user_id,
        "product_details": {
            "id": response.id,
            "name": response.name,
            "price": response.price
        },
        "source": "gRPC"
    }
