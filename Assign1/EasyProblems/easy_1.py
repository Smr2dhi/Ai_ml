name=input("Enter your name: ")
age=int(input("Enter your age: "))
salary=float(input("enter your salary: "))
print(f"Hello,{name}")
print(f"Age : {age}")
print(f"Salary :{salary} ")
print(type(name),type(age), type (salary))
 
def is_permanent(value):
    responses={
        "Yes":'True',
        "No":'False'
    }
    return responses.get(value)
is_permanentPerson= (input("Are you permanent: "))
print(is_permanentPerson)
print(type(is_permanentPerson))
value=is_permanent(is_permanentPerson)
print(value)
