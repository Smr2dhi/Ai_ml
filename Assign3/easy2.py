import json

# metadata = { 
#     "document_id": 1, 
#     "name": "HR Policy", 
#     "category": "HR", 
#     "uploaded_by": "Admin", 
# } 
# with open("metadata.json","w")as file:
#     data=json.dumps(metadata,indent=4)
#     file.write(data)
#     print("Metadata saved...")

# with open("metadata.json","r")as file:
#     data =json.load(file)
# print(data)

# try:
#     with open("missing.json","r") as  file:
#         data=json.load(file)
# except FileNotFoundError:
#     print("no such file exist!!--startng fresh ")


metadata=[{"document_id": 1, 
    "name": "HR Policy", 
    "category": "HR", 
    "uploaded_by": "Admin"}]

with open ("metadata.json","w")as file:
    json.dump(metadata,file,indent=4)

with open("metadata.json", "r") as file:
    data = json.load(file)

print("List:", data)
print("type of list:",type(data))
