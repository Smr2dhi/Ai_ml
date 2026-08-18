from .models.student import Student,student_from_dict
from .services.student_service import StudentService
from .utils.storage import save_students,load_students

service =StudentService()
while True:
    print("""
        === Student Management v2 === 
        1. Add Student 
        2. View All Students 
        3. Search by Name 
        4. Class Statistics 
        5. Exit 

    """)
    choice= int(input("Enter your choice: "))

    if choice==1:
        name=input("name: ")
        rollno=int(input("Roll: "))
        marks=float(input("Marks: "))
        result=service.add_student(name,rollno,marks)

        if result:
            print("Student Added---")
        else:
            print("Rollno alreaady exists")

    elif choice==2:
        students=service.list_students()

        if not students:
            print("No student added")
        else:
            for student in students:
                print(f"{student.name} ,{student.roll}, {student.marks}")

              

    elif choice==3:
        search_name=input("Enter the name to search: ")

        student=service.search_by_name(search_name)

        if student:
            print(f"Name: {student.name}")
            print(f"Roll: {student.roll}")
            print(f"Marks: {student.marks}")

        else:
            print("No such student exists")

    elif choice==4:
        student=service.statistics()

        if student is None:
            print("No student exists--")

        else:
            print(f"Total students: {student['total_students']}")
            print(f"Class average  : {student['average']}")
            print(f"Topper         : {student['topper']}")
            print(f"Pass percentage: {student['pass_percentage']}%")

    elif choice==5:
        break

    else:
        print("invalid option")

    