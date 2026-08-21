from pydantic import BaseModel,Field
import json

class Address(BaseModel):
    city:str
    country:str

class Customer(BaseModel):
    name:str
    email:str
    address:Address

class Order(BaseModel):
    order_id:int
    customer:Customer
    items:list[str]
    total:float=Field(gt=0)
    delivered:bool=False

order_data = { 
    "order_id": 501, 
    "customer": { 
        "name": "Sara", 
        "email": "sara@email.com", 
        "address": {"city": "Delhi", "country": "India"}, 
    }, 
    "items": ["laptop", "mouse"], 
    "total": 82500.0, 
} 

print("----Deserialize-----")
obj1=Order(**order_data)
print(obj1)

print("city:",obj1.customer.address.city)

print("----Serialize----")
obj2=obj1.model_dump()
print(obj2)

print(obj1.delivered)
