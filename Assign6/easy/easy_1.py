from pydantic import BaseModel

class Employee(BaseModel):
    name:str
    age:int
    salary:float
    active:bool

user=Employee(
    name='John',
    age=30,
    salary=500004.9,
    active=True
)

print(user)
print(user.model_dump())
print(user.model_dump_json())

user2=Employee(
    name="sam",
    age="28",
    salary=898737.90,
    active=True
)
print(user2.age, type(user2.age))