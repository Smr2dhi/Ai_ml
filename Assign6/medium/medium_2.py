from pydantic import BaseModel,Field
from fastapi import FastAPI

class ProductCreateRequest(BaseModel):
    name:str
    price:float=Field(gt=0)
    category:str="general"
    stock:int =Field(gt=0)

class ProductResponse(BaseModel):
    product_id:int
    name:str
    price:float
    category:str
    stock:int


app=FastAPI()
products=[]

@app.post("/products",response_model=ProductResponse)
def product_request(product:ProductCreateRequest):
    product_id=len(products)+1
    name=product.name
    price=product.price
    category=product.category
    stock=product.stock

    product_response={
        "product_id":product_id,
        "name":name,
        "price":price,
        "category":category,
        "stock":stock
    }
    products.append(product_response)

    return product_response

@app.get("/products/{product_id}",response_model=ProductResponse)
def get_data(product_id:int):
    for product in products:
        if product["product_id"]==product_id:
            return product

