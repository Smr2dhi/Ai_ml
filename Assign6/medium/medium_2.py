from pydantic import BaseModel,ValidationError,Field
from fastapi import FastAPI

class ProductCreateRequest(BaseModel):
    name:str
    price:float=Field(gt=0)
    category:str="general"

class ProductResponse(BaseModel):
    product_id=int
    name:str
    price:float
    category:str


app=FastAPI=[]