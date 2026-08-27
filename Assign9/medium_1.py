import json

data={
"policy_number": "P20443",
"customer_name": "Anita Deshmukh",
"premium_amount": 24500
}




try:
    
    print("Valid json")
    print(data)
except json.JSONDecodeError:
    print("invalid json")

