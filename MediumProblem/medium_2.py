policies=[
   {"policy_number": "P1001", "customer": "John", "premium": 1500, "active": True},
    {"policy_number": "P1002", "customer": "Sara", "premium": 2200, "active": True},
    {"policy_number": "P1003", "customer": "Mike", "premium": 1800, "active": False},
]
count=0
found=False
while True:
    policyNum = input("Enter your Policy Number(q to quit): ")
 
    if policyNum == "q":
        break
    for policy in policies:
        if policyNum == policy["policy_number"]:
            print("Policy Number:", policy["policy_number"])
            print("Customer:", policy["customer"])
            print("Premium:", policy["premium"])
            print("Active:", policy["active"])
            found=True
            break
 
		
if not found:
    print("Not found") #Printing 3 times
    count+=1
print(count)