import json

employee = { 
    "employee_id": 101, 
    "name": "John Smith", 
    "department": "IT", 
    "skills": ["Python", "FastAPI", "Azure"], 
} 

json_data=json.dumps(employee,indent=4)
print(json_data)

print(f"Type of original dict: {type(employee)}")
print(f"type of json String: {type(json_data)}")

json_deserialize=json.loads(json_data)

print("Restored name: ",json_deserialize["name"])
print("Second skill: ",json_deserialize["skills"][1])

json_deserialize.update({"salary":5000})

json_serialized = json.dumps(json_deserialize)
print(json_serialized)

try:
    json.loads("{this is broken}")
except json.JSONDecodeError:
    print("Real api responses arw sometimes malformed")