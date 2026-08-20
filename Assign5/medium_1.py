import requests
import json
import os
import sys
from logs.logger import session_logger,global_logger


url="https://jsonplaceholder.typicode.com/users/"
try:
    response=requests.get(url)
    print(response.status_code)

    data=response.json()

    for user in data:
        print(f"User data are: {user['name']} | {user['email']}| {user["address"]["city"]}")
        session_logger.info(f"User data are: {user['name']} | {user['email']}| {user["address"]["city"]}")

except requests.exceptions.RequestException as e:
    global_logger.error("Error while requesting the url")
    print("Error while requesting the url")

print("_________________________________________")
# Taking user input for 2nd api request---
try:
    userId=input("enter a userID:")

    response=requests.get(url+userId)
    session_logger.info(f"response status of api:{response.status_code}")

    if response.status_code ==200:
        data1=response.json()

        print(f"successful response:{data1['name']} | {data1['email']}| {data1["address"]["city"]} | {data1["company"]["name"]}")
        session_logger.info(f"successful response:{data1['name']} | {data1['email']}| {data1["address"]["city"]} | {data1["company"]["name"]}")

    else:
        global_handler.warning(f"userID: {userId} not found")
        sys.exit()

except requests.exceptions.RequestException as e:
    global_logger.error("error while requesting the user")   

    

try:
    file_path=os.path.dirname(__file__)
    file_name=os.path.join(file_path,f"customer_{userId}.json")
    

    with open(file_name,"w")as file:
        json.dump(data1,file,indent=4)

        session_logger.info(f"File saved to customer{userId}.json")

except OSError as e:
    global_logger.warning(f"Error while saving the file:{e}")

print()
print("all unique cities ------")

cities=set()
for user in data:
    cities.add(user['address']['city'])

print(cities)