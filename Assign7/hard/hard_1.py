from pydantic import BaseModel,Field,field_validator
from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
import logging
import os

log_file= os.path.join(os.path.dirname(__file__),"hard_1.log")


logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s- %(levelname)s -%(message)s"
    )


logger=logging.getLogger(__name__)
app=FastAPI()

@app.exception_handler(Exception)
async def global_handler(request:Request, exc:Exception):
    logger.error("Unexpected error on %s: %s",request.url,exc)
    return JSONResponse(
        status_code=500,
        content={
            "error":"Something went wrong"
        }
    )



class StudentCreateRequest(BaseModel):
    student_id:str=Field(min_length=4)
    name:str=Field(min_length=3)
    age:int=Field(gt=0,le=60)
    email:str

    @field_validator("email")
    @classmethod
    def validate_email(cls,value):
        if   "@" not in value:
            raise ValueError("invalid email")
        return value


    @field_validator("student_id")
    @classmethod
    def validate_studentid(cls,value):
        if not value.startswith("STU"):
            raise ValueError(" Student ID must start with STU" )
        return value
            
        
class StudentResponse(BaseModel):
    student_id:str
    name:str
    age:int
    email:str


class StudentService:
    def __init__(self):
        self.student_data=[]

    def get_all(self):
        return self.student_data

    def get_by_id(self,student_id):
        for data in self.student_data:
            if data["student_id"]==student_id:
                return data
        return None


    def create(self,student_id,name,age,email):
        student={
            "student_id":student_id,
                "name":name,
                "age":age,
                "email":email
            
        }
        self.student_data.append(student)
        return student

    def update(self,student_id,name,age,email):
        student=self.get_by_id(student_id)
        if student is None:
            return None

        student["name"]=name
        student["age"]=age
        student["email"]=email
        return student

        
    def delete(self,student_id):
        student= self.get_by_id(student_id)
        if student is None:
            return False
        self.student_data.remove(student)
        return True
       

students=StudentService()

def not_found_error(student_id):
    logger.warning(f"student {student_id} not found")
    return HTTPException(
        status_code=404,
        detail=f"Student {student_id} not found"    
        )

@app.get("/students",response_model=list[StudentResponse])
def get_allstudent():
    return students.get_all()  

@app.get("/students/{student_id}",response_model=StudentResponse)
def get_students(student_id:str):
    student= students.get_by_id(student_id)

    if student is None:
        raise not_found_error(student_id)
    return student

@app.post("/students",response_model=StudentResponse)
def create_stuent(request:StudentCreateRequest):

    if students.get_by_id(request.student_id)is not None:
        
        logger.warning(f"Duplicate student {request.student_id}")

        raise HTTPException(
            status_code=400,
            detail="Student"+request.student_id+"already exist"
        )

    
    student= students.create(
        request.student_id,
        request.name,
        request.age,
        request.email
    )
    logger.info("Created student %s", request.student_id)
    return student

@app.put("/students/{student_id}")
def update_student(student_id: str, request: StudentResponse):

    student = students.update(
        student_id,
        request.name,
        request.age,
        request.email
        )
    if student is None:
        raise not_found_error(student_id)
    logger.info("Updated student %s", student_id)
    return student
    
@app.delete("/students/{student_id}")
def delete_student(student_id:str):
    deleted=students.delete(student_id)

    if not deleted:
        raise not_found_error(student_id)
    logger.info("Deleted student %s", student_id)
    return{
        "message":"Student"+student_id+"deleted"
    }
    