from fastapi import FastAPI,HTTPException
import logging

from logs.logger import session_logger

app=FastAPI()

accounts = { 
    "ACC1": {"customer": "John", "balance": 5000}, 
    "ACC2": {"customer": "Sara", "balance": 0}, 
} 
@app.get("/accounts/{account_id}")
def search_account(account_id:str):
    if account_id in  accounts:
        
            return {
                "account_id":account_id,
                "customer":accounts[account_id]["customer"],
                "balance":accounts[account_id]["balance"]
            }
        
    raise HTTPException(
        status_code=404,
        detail=f"account {account_id} not found"
    )

@app.get("/accounts/{account_id}/free-ratio")
def get_free_rations(account_id:str):
    
        balance=accounts[account_id]["balance"]

        return{
                "free_ration":100/balance
        }
   
    
