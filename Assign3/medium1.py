import requests
import json
def UserFetch(userId):
    url=f"https://jsonplaceholder.typicode.com/users/{userId}"
    responses= requests.get(url,timeout=10)

    if responses.status_code ==200:
        print("success!!")

        data=responses.json()
        return data

    else:
        raise requests.exceptions.HTTPError(
            f"Api request failed : {responses.status_code} Client Error: Not found for url:{url} "
        )


def fileHandling(userData):
    with open("user.json","w")as file:
        json.dump(userData,file,indent=4)
        print(file)
        print("Data stored in file")

    
while True:
    userId= input("enter your id('q' for quit): ")
    if userId.lower() =='q':
        break
    userId=int(userId)
    try:
        userData=UserFetch(userId)
        print(f"user name: {userData['name']} ")
        print (f"emailId: {userData['email']} ")
        print  (f"city: {userData['address']['city']}" )
        print  (f"companyName: {userData['company']['name']}")

        fileHandling(userData)
    except requests.exceptions.RequestException as e:
        print("Error:",e)

        res=input("Do you want to retry(y/n): ")

        if res.lower() =='y':
            pass
        elif res.lower()=='n':
            break


