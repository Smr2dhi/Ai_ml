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
def policy():
    return{
    "services":"Policy API",
    "version":"1.0",
    "endpoints":[]
}