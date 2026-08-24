# •	The duplicate check cannot live in the model —
#  the model sees one request at a time. Business state
#  checks belong in the endpoint. 
# That is the input-vs-business validation boundary.


from pydantic import BaseModel,field_validator,Field

from fastapi import FastAPI,HTTPException

app=FastAPI()

class UserRegistrationRequest(BaseModel):
	name:str=Field(min_length=3)
	age:int
	email:str
	password:str=Field(min_length=8)
	phone:str=Field(min_length=10,max_length=10)

	@field_validator("age")      #field_validator() → Custom rules  # When the rule requires your own Python logic, use field_validator.
								
	@classmethod              
	def validate_age(cls,value):			# . @classmethod → How the validator function is called @classmethod is not the validation itself.
											# cls   → UserRegistrationRequest  # value → actual age
		if value<18:
			raise ValueError(
				"age must be at least 18"
			)
		return value

	@field_validator("email")
	@classmethod
	def validate_email(cls,value):
		if "@" not in value:
			raise ValueError("invalid Email") 
		return value

	@field_validator("password")
	@classmethod
	def validate_password(cls,value):
		for char in value:
			if char.isdigit():
				return value
			 
		raise ValueError("password msut conatin at least one digit")

	@field_validator("phone")
	@classmethod
	def validate_phone(cls, value):
		for data in value:
			if not data.isdigit():
				raise ValueError("Phone must contain only digits")
		return value


registered_emails=[]
@app.post("/register")
def create_user(user:UserRegistrationRequest):
	
	if user.email in registered_emails:
		raise HTTPException (
			status_code=400,
			detail="Email already registered"
		)
	
	registered_emails.append(user.email)
	return {
				"message":"User registered",
				"email":user.email
			}
