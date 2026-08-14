import requests
import json

def apihandling():
   
        url = "https://jsonplaceholder.typicode.com/users/"

        response = requests.get(url, timeout=10)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            print("Success!!")

            data = response.json()

            count = len(data)
            print("Users returned:", count)

            for row in data[:3]:
                print(f"{row['name']} ({row['email']})")
                print(f"City: {row['address']['city']}")
        else:
            print("Invalid")


try:
    apihandling()

except Exception as e:
    print(e)