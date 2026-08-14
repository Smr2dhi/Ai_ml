import json
import copy
import time

library = { 
    "documents": [ 
        {"id": 1, "name": "HR Policy",     "category": "HR",   "tags": {"leave", "policy"}}, 
        {"id": 2, "name": "API Standards", "category": "Tech", "tags": {"api", "python", "rules"}}, 
    ], 
    "categories": {"HR", "Tech"}, 
} 

# with open("lib.json","w") as file:
#     json.dump(library,file)
#     print("done")

# giving error :Here the TypeError occurs because 
# tags and categories are Python sets, and JSON doesn't 
# support set directly.

def libToJson(library):
    newLibrary =copy.deepcopy(library)

    newLibrary["categories"]= sorted(newLibrary["categories"])

    for doc in newLibrary["documents"]:
        doc["tags"]=sorted(doc["tags"])

    return newLibrary


def fileHandling(newLib):
    newLib["saved_at"]=time.strftime("%Y-%m-%d %H:%M:%S")

    with open("lib.json","w")as file:
        json.dump(newLib,file,indent=4)
    print ("successfully file saved lib.json")

def jsonToLib(newLib):
    revLibrary =copy.deepcopy(newLib)

    print("Library saved at: " ,revLibrary["saved_at"])


    revLibrary["categories"]= set(revLibrary["categories"])

    for doc in revLibrary["documents"]:
        doc["tags"]=set(doc["tags"])


    return revLibrary


print("Tags type in file data:",type(library["documents"][0]["tags"]))

newLib=libToJson(library)
print("Tags type in file data:",type(newLib["documents"][0]["tags"]))

fileHandling(newLib)

revLib=jsonToLib(newLib)
print("Tags type in file data:",type(revLib["documents"][0]["tags"]))


print('restored data is still behnaving like set after changes("api"in revLib["documents"][1]["tags"]):' ,"api"in revLib["documents"][1]["tags"])
