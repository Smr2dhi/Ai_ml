registrations = ["python", "ai", "python", "fastapi", "ai", "python", "sql"] 
print(registrations)

the_set= set(registrations)
print(tuple(registrations))
the_tuple= tuple(registrations)

print("-------")
registrations.append("java")
the_tuple.append("Java")

print(the_set)
for item in the_set:
    print(f"- {item}")
count= len(the_set)

count2 =len(registrations)
print ("Duplicate removed: " ,count2-count)

course=input("Enter one course name : ")
if course in the_set:
    print("Course exist in the set")
else:
    print ("Course does not exist !!")
