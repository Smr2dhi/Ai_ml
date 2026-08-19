# Domain: jsonplaceholder.typicode.com
# Resource: users
# Resource ID: 1
from logs.logger import global_logger,session_logger
import requests

url="https://jsonplaceholder.typicode.com/users/"
try:
    user=input("Enter the user id between (1-10): ")

    if not user.isdigit() or not 1<=int(user)<=10:
        raise ValueError ("User Id must be between 1 and 10")
    response=requests.get(
       url+user
    )

    if response.status_code==200:
        data=response.json()
        print(f'name: {data["name"]}')
        print(f'email: {data["email"]}')
        print(f'city: {data["address"]["city"]}')

    else:
        raise Exception(f"Failed during the response {response.status_code}")

except Exception as e:
    print(f"Error handled :{e}")


except ValueError as e:
    print(f"Error handle:{e}")

