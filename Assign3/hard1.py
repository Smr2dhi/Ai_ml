import json
import requests


local_employees = [ 
    {"id": 1, "name": "John Smith", "email": "john.smith@company.com", "source": "local"}, 
    {"id": 2, "name": "Sara Iyer", "email": "sara.iyer@company.com", "source": "local"}, 
] 


def loadLOcalEmployees():
    with open("employees.json", "w") as file:
        json.dump(local_employees, file, indent=4)
        print("File created!!")

    try:
        with open("employees.json", "r") as file:
            data = json.load(file)
            print(data)

    except FileNotFoundError as e:
        print("No local file exist!!", e)


info = []                     


def FetchPartnerDir():           
 
    try:
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url, timeout=10)

        response.raise_for_status()    
        data = response.json()


        for user in data:

            found=False

            for i in info:
                if  (user['email']==i["email"]  ):
                    print("user already exists")
                    found=True
                    break
                
            if found==False:
                info.append(
                        {
                            "id":user["id"],
                            "name":user["name"],
                            "email":user["email"],
                            "source":"api"

                        }
                    )

    except requests.exceptions.RequestException as e:
        print("API request failed:", e)       




def listAll():
    for row in info:
        if not info:
            print("Info is empty")
        else:
            print(f"[Local]: ,{row['name']},{row['email']}")


def searchByName(name):
    for row in info:
         
        if row['name'].lower()==name.lower():
            print(row)
        else:
            print("No such name exist")

def saveMergedDirectory():
    with open("directory.json","w")as file:
        json.dump(info,file,indent=4)
        print("File cretaed")

    with open("directory.json","r")as file:
        data=json.load(file)
        print("Loaded data: ",data)

    


while True:
    print("""
=== Employee Directory === 
1. Load Local Employees 
2. Fetch Partner Directory (API) 
3. List All 
4. Search by Name 
5. Save Merged Directory 
6. Exit 
""")
    userInput = int(input("Enter your choice: "))

    if userInput == 1:
        loadLOcalEmployees()

    elif userInput == 2:
        FetchPartnerDir()
        print(info)
        

    elif userInput == 3:
        listAll()

    elif userInput == 4:
        user=input("Enter the name to search: ")
        searchByName(user)

    elif userInput == 5:
        saveMergedDirectory()

    elif userInput == 6:
        break

    else:
        print("Invalid userInput")