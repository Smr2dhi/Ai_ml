from pydantic import BaseModel,Field,ValidationError

from fastapi import FastAPI

app=FastAPI()

class UserProfileRequest(BaseModel):
	name:str=Field(min_length=3)
	age:int=Field(gt=0,le=100)
	email:str
	department:str=Field(le=50)

@app.post("/users")
def create_user(user:UserProfileRequest):
	return  {
		"message": "Profile accepted",
		  "name": user.name, 
		  "age": user.age
		  }
