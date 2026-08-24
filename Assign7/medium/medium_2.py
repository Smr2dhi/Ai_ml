from pydantic import BaseModel,Field
from fastapi import FastAPI,HTTPException

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
		return self.products

	
	def get_by_id(self,product_id):
		for data in self.products:
			if data["product_id"] == product_id:
				return data

		return None

	def create(self,name,price):
		product={
			"product_id":self.next_id,
			"name":name,
			"price":price,
		}
		self.products.append(product)
		self.next_id+=1

		return product

		
	def update(self,product_id,name,price):
		for data in self.products:
			if product_id == data["product_id"]:
				data["name"]=name
				data["price"]=price
				return data
		return None

			

	def delete(self,product_id):
		for data in self.products:
			if data["product_id"]==product_id:
				self.products.remove(data)
				return data

		return None


product_service=ProductService()


@app.get("/products",response_model=list[ProductResponse])
def get_products():

	products=product_service.get_all()

	if not products:
		raise HTTPException(status_code=404,detail="no products found")
	return products

@app.get("/products/{product_id}",response_model=ProductResponse)
def get_product_by_id(product_id :int):

	product=product_service.get_by_id(product_id)

	if product is None:
		raise HTTPException(status_code=404,detail="Product not found")
	return product
	


@app.post("/products",response_model=ProductResponse)
def add_products(product:ProductCreateRequest):

	return product_service.create(
		product.name,
		product.price
	)
	


@app.put("/products/{product_id}",response_model=ProductResponse)
def update_product(product_id:int,product:ProductCreateRequest):

	updated=product_service.update(
		product_id,product.name,product.price)

	if updated is None:
		raise HTTPException(status_code=404,detail="product not found")

	return updated

@app.delete("/products/{product_id}",response_model=ProductResponse)
def delete_product(product_id:int):

	deleted_product=product_service.delete(product_id)

	if deleted_product==None:
		raise HTTPException(status_code=404,detail="Product not found")

	return deleted_product

