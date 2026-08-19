import os 
from logs.logger import session_logger,global_logger
from Assign4.hard_1.utils.storage import load_students,save_students
from Assign4.hard_1.models.student import Student,student_from_dict
 
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
STUDENT_FILE=os.path.join(BASE_DIR,"students.json") 
 
class StudentService:  
    def __init__(self):  
        self.students_list=[]  
  
        try:  
            session_logger.debug("Loading students from file") 
 
            for data in load_students(STUDENT_FILE):  
                student=student_from_dict(data)  
                self.students_list.append(student) 
 
            session_logger.info("Students loaded successfully") 
 
        except Exception:  
            global_logger.error("Failed to load student from file")  
            raise  
  
    def add_student(self,name,roll,marks):  
 
        session_logger.debug(f"Trying to add student: {name}, roll={roll}") 
 
        for student in self.students_list:  
            if student.roll==roll:  
                global_logger.warning(f"Student with roll number {roll} already exists")  
                return False  
  
        s1=Student(name,roll,marks)  
        self.students_list.append(s1)  
  
        student_data=[]  
         
        for student in self.students_list:  
            student_data.append(student.to_dict()) 
 
        try:  
            save_students(student_data,STUDENT_FILE) 
 
            session_logger.info(f"Student added successfully: {name}") 
 
            return True  
 
        except Exception:  
            global_logger.error(f"Failed to save student with roll number {roll}")  
            raise 
  
    def list_students(self):  
        session_logger.debug("Listing all students") 
        return self.students_list  
  
    def search_by_name(self,name):  
        session_logger.debug(f"Searching student by name: {name}") 
 
        for student in self.students_list:  
            if student.name.lower()==name.lower():  
                session_logger.info(f"Student found: {name}") 
                return student  
  
        global_logger.warning(f"Student not found: {name}") 
        return None 
     
    def statistics(self):  
        session_logger.debug("Calculating student statistics") 
 
        if len(self.students_list)==0:  
            global_logger.warning("Statistics requested but no students exist")  
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
  
        session_logger.info("Student statistics calculated") 
        return Student_satistics