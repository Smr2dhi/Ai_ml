from models.student import Student
from utils import greet
from models.employee import Employee

print(greet("Samriddhi"))

s1=Student("Sam","AI")
print(f"Student created: {s1.name} ({s1.branch})")

print(s1.introduce())

print("-------------")
e1=Employee("Khushi","Tech")
print(f"Student cretaed: {e1.name} ({e1.departement})")

print(e1.Introduce())