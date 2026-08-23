from pydantic import BaseModel,Field
from fastapi import FastAPI
from typing import Literal

app=FastAPI()
class AccountRequest(BaseModel):
	customer_name:str
	account_type:str="saving"
	opening_balance:float=Field(gt=0)

class AccountResponse(BaseModel):
	account_number:int
	customer_name:str
	account_type:str
	balance:float

class TransactionRequest(BaseModel):
	account_number:int
	transaction_type:str="deposit"
	amount:float=Field(gt=0)

class TransactionResponse(BaseModel):
	transaction_id:int
	account_number:int
	status:str
	new_balance:float

accounts_dict={}

@app.post("/",response_model=AccountResponse)
def create_account(account:AccountRequest):
	account_number=len(accounts_dict)+1001

	account_data = {
		"account_number":account_number,
		"customer_name":account.customer_name,
		"account_type":account.account_type,
		"balance":account.opening_balance,
	}
	accounts_dict[account_number]=account_data
	return account_data

@app.get("/accounts/{account_number}")
def get_account(account_number:int):

	if account_number in accounts_dict:
		return accounts_dict[account_number]

account_transaction=[]
@app.post("/transactions",response_model=TransactionResponse)
def add_transaction(new_transaction:TransactionRequest):



	if new_transaction.account_number  in accounts_dict:
		print(new_transaction.transaction_type)

		if new_transaction.transaction_type=="deposit":
			accounts_dict[new_transaction.account_number]["balance"]+=new_transaction.amount
			status="success"

		elif new_transaction.transaction_type=="withdraw":

			if accounts_dict[new_transaction.account_number]["balance"]>=new_transaction.amount:
				accounts_dict[new_transaction.account_number]["balance"]-=new_transaction.amount
				status="sucess"

			else:
				status="Insufficient amount"

		else:
			status="declined -unknown transaction type"
			
				

		transaction={
				"transaction_id":len(account_transaction)+1,
					"account_number":new_transaction.account_number,
					"status":status,
					"new_balance":accounts_dict[new_transaction.account_number]["balance"]
			}
		account_transaction.append(transaction)
		return transaction
		
@app.get("/accounts/statement/{account_number}")
def get_statement(account_number:int):
	statement=[]

	for transaction in account_transaction:
		if transaction["account_number"]==account_number:
			statement.append(transaction)

	return statement