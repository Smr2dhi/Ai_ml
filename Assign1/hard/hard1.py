 
students=[]
roll_no=set()
 
def addStudent():
    while True:
        rollno= input(f"Enter your roll_no (or for quit 'q'): ")
 
        if rollno == "q":
            break

        try:
             rollno=int(rollno)
        except ValueError:
            print("Enter a valid num ")
            continue
 
        if rollno in roll_no:
            print("Rollno already exist!")
            continue
 
        roll_no.add(rollno)
       
   
        name=input("Enter your name: ")
        try:
            subjects= int(input("How many subjects ?: "))
        except ValueError:
            print("Enter a valid num")
            continue
       
        marks=[]
 
        for i in range(subjects):
            try:
                mark=int(input(f"Enter your marks {i+1}: "))
                marks.append(mark)
            except ValueError:
                print("enter marks in number")
                continue
 
        student={
            "name": name,
            "roll_no":rollno,
            "marks":marks
 
        }
        students.append(student)
 
 
 
def printStudents():
    if not students:
        print("please first add at least one student")
        return
    print(students)
 
def searchByName():
    inputName=input("Enter the name of student you want to searc..?: ")
 
    isStudentFound = False
 
    for student in students:
        if student["name"].lower()==inputName.lower():
            print(student)
            isStudentFound = True
 
    if not isStudentFound:
        print("No such student exist..")
 
 
           
def studentStatistics():
    if not students:
        print("Please enter students's data")
        return
 
    print("printing student's name:  ")
    for student in students:
        print( student['name'] )
    totalMarks=0
    totalSubjects=0
 
    for student in students:
        totalMarks+=sum(student["marks"])
        totalSubjects+=len(student["marks"])
 
 
    classAvg= totalMarks/totalSubjects
    print("Avg of Class: ",classAvg)
 
    print("Student with highest score: ")
    highestScore=0
 
    for student in students:
        total= sum(student["marks"])
        percent =(total/len(student["marks"]))
 
        if total > highestScore:
            highestScore=total
            highestStudent=student
 
 
    print("Topper : " ,highestStudent["name"],highestScore)
    print("Total percent: ",percent,"%")
 
 
def removeStudent():
    if not students:
        print("no stuents added yet")
        return
    try:
        value = int(input("enter the rollno of student to delete:"))
   
    except ValueError:
        print("Enter a valid num")
        return
    
    for student in students:
        if student["roll_no"] ==value:
            students.remove(student)
            print(f"student with roll_no:{student['roll_no']} removed: ")
            return
       
 
 
 
 
print("=== Student management ===")
 
value= input("Enter your name: ")
print("Hello!!",value)
while True:
    print("Select choice: ")
    print("""
    1. Add Student
    2. View All Students
    3. Search by Name
    4. Class Statistics
    5. Exit
    6. remove Student by RollNo
    """)
    try:
        choice = int (input("select option: "))
    except ValueError:
        print("please enter a num")
        continue
    if choice == 1:
        addStudent()
    elif choice ==2:
        printStudents()
    elif choice ==3:
        searchByName()
    elif choice ==4 :
        studentStatistics()
    elif choice ==5  :
            print("bye bye !")
            break
    elif choice ==6:
        removeStudent()
       
    else:
        print("invalid Input !!")
 
 
 
 
 