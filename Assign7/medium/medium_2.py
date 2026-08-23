from pydantic import BaseModel,Field
from fastapi import FastAPI

app=FastAPI()

class ProductCreateRequest(BaseModel):
	name:str=Field(min_length=1)
	price:float=Field(gt=0)

class ProductResponse(BaseModel):
	product_id:int
	name:str
	price:float
	
class ProductService:
	def __init__(self):
		self.products=[]
		self.next_id=1

	def get_all(self):
		pass

	def get_by_id(self,product_id):
		pass

	def create(self,name,price):
		pass

	def update(self,product_id,name,price):
		pass

	def delete(self,product_id):
		pass

product_service=ProductService

@app.get("/products")
def get_products():
	return product_service.get_all()

@app.get("/products/{id}")
def get_Product_by_id():
	return product_service.get_by_id()

@app.post("/products")
def add_products():
	return product_service.create()

@app.put("/products/{id}")
def update_product():
	return product_service.update()

@app.delete("/products/{id}")
def delete_product():
	return product_service.delete()
