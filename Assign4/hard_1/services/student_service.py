from utils.storage import load_students,save_students
from models.student import Student,student_from_dict

class StudentService:
    def __init__(self):
        self.students_list=[]

        for data in load_students("Assign4/hard_1/students.json"):
            student=student_from_dict(data)
            self.students_list.append(student)


    def add_student(self,name,roll,marks):
        for student in self.students_list:
            if student.roll==roll:
                return False

        s1=Student(name,roll,marks)
        self.students_list.append(s1)

        student_data=[]
        
        
        for student in self.students_list:
            student_data.append(student.to_dict())

        save_students(student_data,"Assign4/hard_1/students.json")
        return True

    def list_students(self):
        return self.students_list

    def search_by_name(self,name):
        for student in self.students_list:
            if student.name.lower()==name.lower():
                return student
        return None
    
    def statistics(self):
        if len(self.students_list)==0:
            return None
   
        totalStudent=len(self.students_list)

        total_marks=0
        pass_count=0
        topper=self.students_list[0]

        for student in self.students_list:
            total_marks+=student.marks

            if student.marks>=40:
                pass_count+=1

            if student.marks>topper.marks:
                topper=student

        average=total_marks/totalStudent
        pass_percentage=(pass_count/totalStudent)*100



        Student_satistics={
            "total_students":totalStudent,
            "average":average,
            "topper":topper.name,
            "pass_percentage":pass_percentage
        }

        return Student_satistics