from pydantic import BaseModel,Field,field_validator
from fastapi import FastAPI,HTTPException

import logging
import os

log_file=os.path.join(os.path.dirname(__file__),"hard_2.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s -%(levelname)s - %(message)s"

)

logger=logging.getLogger(__name__)


app= FastAPI()

class AccountCreateRequest(BaseModel):
    account_id:str=Field(min_length=4)
    customer:str=Field(min_length=3)
    opening_balance:float=Field(ge=0)

class TransactionRequest(BaseModel):
    tx_type:str
    amount:float=Field(gt=0)

    @field_validator("tx_type")
    @classmethod
    def validate_ext(cls,value):
        if value in("deposit","withdraw") :
            return value
        else :
            raise ValueError("tx_type must be deposit or withdraw")

class BankService:
    def __init__(self):
        self.accounts={}

    def create_account(self,account_id,customer,opening_balance):
        account={
            "account_id":account_id,
            "customer":customer,
            "balance":opening_balance,
            "transactions":[]
        }

        self.accounts[account_id]=account
        logger.info(f"Account created {account_id}")
        return account

    def get_account(self,account_id):
        return self.accounts.get(account_id)
        

    def apply_transaction(self,account_id,tx_type,amount):
        account=self.get_account(account_id)

        if account is None:
            return None

        if tx_type=="deposit":
            account["balance"]+=amount

        elif tx_type=="withdraw":
            if amount>account["balance"]:
                logger.warning(f"Insufficient funds {account_id}")
                return None
            account["balance"]-=amount

        account["transactions"].append({
            "tx_type":tx_type,
            "amount":amount
            })
        
        logger.info(
            f"Transaction {tx_type} of {amount} applied to {account_id}"
          )
        return account

    def delete(self,student_id):
        account=self.get_account(student_id)
        if account is None:
            return False
        self.accounts.pop(student_id)
        return True
    

account_obj=BankService()          

@app.post("/accounts")
def create_account(request:AccountCreateRequest):
    if account_obj.get_account(request.account_id) is not None:

        logger.warning("Account_id already exists !!")
        raise HTTPException(
            status_code=400,
            detail="account already exists"
        ) 

    account=account_obj.create_account(
        request.account_id,request.customer,request.opening_balance
    )

    return {
        "account_id":account["account_id"],
        "customer":account["customer"],
        "balance":account["balance"]
    }


@app.get("/accounts/{account_id}")
def get_account(account_id:str):

    account=account_obj.get_account(account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found"
        )

    return {
        "account_id":account["account_id"],
        "customer":account["customer"],
        "balance":account["balance"]
    }


@app.post("/accounts/{account_id}/transactions")
def transaction_account(account_id:str,request:TransactionRequest):

    account=account_obj.get_account(account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found"
        )

    account=account_obj.apply_transaction(
        account_id,
        request.tx_type,
        request.amount
    )

    if account is None:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )

    return {
        "account_id":account["account_id"],
        "balance":account["balance"]
    }


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id:str):

    account=account_obj.get_account(account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found"
        )

    return account["transactions"]


@app.delete("/accounts/{account_id}")
def delete_account(account_id:str):
    deleted=account_obj.delete_account(account_id)

    if deleted is False:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found"
            )
    return {
        "message":f"Account {account_id} deleted successfully"
            }