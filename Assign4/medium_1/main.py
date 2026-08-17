import logging

from services.student_service import Studentservice
from models.employee import Employee


service =Studentservice()


s1= service.create_students("John","CSE")
s2=service.create_students("Priya","AI")


e1=Employee("Sam","IT")

print("Employee created","Name: ",e1.name,", Department: ",e1.department)

print()

print(f"Hello {s1.name}")
print(f"Student created: {s1.name} ({s1.branch})")
print(f"Hi, I am {s1.name} from {s1.branch}")

print()

print(f"Hello {s2.name}")
print(f"Student created: {s2.name} ({s2.branch})")
print(f"Hi, I am {s2.name} from {s1.branch}")
while True:
    value = input("Enter the name you want to search: ")

    try:
        searched_student = service.search_by_name(value)
        if searched_student:
            print("Searched student:", searched_student)
            break
        else:
            print("No such student exists")
            
    except ValueError as e:
        print("Error:", e)