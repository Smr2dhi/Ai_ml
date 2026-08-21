import requests
import sys
BASE = "http://127.0.0.1:8000"
passed_count=0
failed_count=0

def check_helper(description,condition):
    global passed_count,failed_count
    if condition:
        print(f"Pass: {description} ")
        passed_count+=1
    else:
        print(f"Fail:{description}")
        failed_count+=1

try:
    health=BASE+"/health"
    info=requests.get(health)

    if info.status_code==200:
        print(info.json())
    else:
        print("error while fetching data")
        sys.exit()

    check_helper("GET /health returns 200 ",info.status_code==200)
    check_helper("GET /health body is {'status':'healthy'} ",info.json()=={"status":"healthy"})

except requests.exceptions.RequestException as e:
    print(f"Request failed duirng health call")

try:
    response=requests.get(BASE+"/students")
    students=response.json()

    check_helper("GET/students returns a non_empty list",response.status_code==200 and isinstance(students,list) and len(students)>=1)

    required_fields={"id","name","marks","city"}
    all_valid=all(
        required_fields.issubset(student.keys())
        for student in students
    )
    check_helper(
        "Every student has id,name,marks,city",
    all_valid
    )


    response_2=requests.get(BASE+"/students/101")
    User=response_2.json()
    check_helper("GET /students/101 name is John",response_2.status_code==200 )


    response_3=requests.get(BASE+"/students/9999")
    
    check_helper("GET /students/99999 reports an error ",response_3.status_code==404)


    response_4=requests.get(BASE+"/students/count")
    counting=response_4.json()

    check_helper("/students/count matches list length", response_4.status_code and counting==len(students))

except requests.exceptions.RequestException as e:
    print("Request failed duirng students call")

try:
    response_5 = requests.get(BASE + "/students", params={"search": "jo"})
    result = response_5.json()

    passes = True

    for s in result:
        if "jo" not in s["name"].lower():
            passes = False

    check_helper(
        " search 'jo' returns only matching names",
        response_5.status_code == 200 and passes,
    )         
        
except requests.exceptions.RequestException as e:
    print(f"Request Failed: {e}")


print()
print("Results:" ,passed_count, "failed_result:", failed_count)