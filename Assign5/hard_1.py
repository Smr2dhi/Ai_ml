from fastapi import FastAPI

app=FastAPI()

policies = [ 
    {"policy_number": "P1001", "customer": "John",  "type": "auto",   "premium": 1500, "active": True}, 
    {"policy_number": "P1002", "customer": "Sara",  "type": "health", "premium": 2200, "active": True}, 
    {"policy_number": "P1003", "customer": "Mike",  "type": "auto",   "premium": 1800, "active": False}, 
    {"policy_number": "P1004", "customer": "Sara",  "type": "life",   "premium": 5000, "active": True}, 
    {"policy_number": "P1005", "customer": "Priya", "type": "health", "premium": 2600, "active": False}, 
] 

@app.get("/")
def home():
    return{
    "services":"Policy API",
    "version":"1.0",
    "endpoints":[]
}

@app.get("/policies")


def get_policies(status:str=""):
    result=[]

    for query in policies:
        if query["active"] and status=="active" :
            result.append(query)

        elif status=="inactive" and not query["active"]:
            result.append(query)

        elif status=="":
            result.append(query)
    
    return{
            "count":len(result),
            "results":result
                }
       
@app.get("/policies/search")
def search_policy(customer:str="",type:str="",max_premium:float=0):
    result=[]
    for user in policies:
        if user["customer"].lower()==customer.lower()  and user["type"].lower()==type.lower()and user["premium"]<=max_premium:
            result.append(user)

    return {
        "count":len(result),
        "result":result}


@app.get("/policies/stats")
def policy_stats():
    total_policies=len(policies)
    active_count=0
    inactive_count=0
    active_preium_total=0

    for policy in policies:
        if policy["active"]==True:
            active_preium_total+=policy["premium"]
            active_count+=1
        elif  policy["active"]==False:
            inactive_count+=1

    return{
            "total":total_policies,
            "active":active_count,
            "inactive":inactive_count,
            "active_premium_total":active_preium_total
        }

@app.get("/policies/{policy_number}")
def get_policy(policy_number):
    for policy in policies:
        if policy["policy_number"]==policy_number:
            return policy

    return {"error:Policy not found"}

@app.get("/policies/customer/{name}")
def get_name(name=str):
    result=[]
    for user in policies:
        if user["customer"].lower()==name.lower():
            result.append(user)
    return result