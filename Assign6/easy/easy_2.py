from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    name:str
    age:int
    phone: Optional[str]=None
    active:bool=True
    plan :str="basic"
    email:Optional[str]=None

Customer_1=Customer(
    name="Rahul",
    age=25
)

print(Customer_1)

Customer_2=Customer(
    name="Priya",
    age=23,
    phone="678900394",
    active=False,
    plan="premium"
)
print(Customer_2)
print("Rahul phone no:",Customer_1.phone)

Customer_3=Customer(
    name="Riya",
    age=20,
    email="smr2dhiya@gamil.com"

)
print(Customer_3)