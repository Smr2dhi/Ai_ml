from fastapi import FastAPI, HTTPException

app=FastAPI()

policies = {
    "P1001": {"customer": "John", "premium": 1500},
    "P1002": {"customer": "Sara", "premium": 2200},
}

@app.get("/policies/{policy_number}")
def search_policy(policy_number:str):

	
	if policy_number in policies:
		policy=policies[policy_number]
		return {
				"policy_number":policy_number,
				"customer":policy["customer"],
				"premium":policy["premium"]
			}
	raise HTTPException(
			status_code=404,
			detail=f"Policy Number {policy_number}  not found"
		)

@app.get("/policies")
def get_all_policies():

	if  not  policies:
		raise HTTPException(
			status_code=404,
			detail="No polices exist yet"
			)
	
	return policies