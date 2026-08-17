from models.student import Student


class Studentservice:
    def __init__(self):
        self.students=[]
        

    def create_students(self,name,branch):
        s1=Student(name,branch)
        self.students.append(s1)
        return s1
       
    def list_student(self):
        return self.students
     

    def search_by_name(self,name):

        if not name.strip():
            raise ValueError("Name cannot be empty")

        for student in self.students:
            if name.lower() == student.name.lower():
                return student.name

        return print("No such student exists")
       


        