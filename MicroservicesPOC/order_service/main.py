import requests
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel

app = FastAPI()

class Order(BaseModel):
    product_id: int
    quantity: int

orders_db = []

@app.post("/order")
def create_order(order: Order):
    product = requests.get(f"http://product_service:8002/product/{order.product_id}").json()
    
    if product["stock"] < order.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")
    
    orders_db.append(order)
    return {"message": "Order created successfully"}