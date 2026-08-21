from pydantic import BaseModel,Field,ValidationError

class BankAccount(BaseModel):
    account_number:str
    holder_name:str
    balance:float = Field(gt=0)
    account_type:str="savings"
    branch_code:int=Field(gt=0)

user=BankAccount(
    account_number="P1001",
    holder_name="Samriddhi",
    balance=78976.90,
    account_type="current",
    branch_code=67

)
print(user)
try:
    user2=BankAccount(
        account_number="P1002",
        holder_name="Ramesh",
        balance="2500.75",
        branch_code=0

    )
    print(user2.balance , type(user2.balance))
    print(user2.branch_code)

except ValidationError as e:
    print("Error: ",e)
