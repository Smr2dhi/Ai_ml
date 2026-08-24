from fastapi import FastAPI, HTTPException
from Assign7.test.models import RegistrationRequest
from Assign7.test.logger_config import get_loggger

app=FastAPI()
logger=get_loggger(__name__)

class DuplicateRegistrationError(Exception):
    pass

registrations=[]

@app.post("/registrations")
def add_student(register:RegistrationRequest):
    try:
        for data in registrations:
            if data.student_id==register.student_id and  data.course== register.course:
                raise DuplicateRegistrationError()

        registrations.append(register)
        logger.info("Student registered")

        return {
            "student_id": register.student_id,
            "student_name": register.student_name,
            "course": register.course,
            "email": register.email
        }

    except DuplicateRegistrationError:
        raise HTTPException(
            status_code=409
        )


@app.get("/registrations/{student_id}")
def return_course(student_id:int):
    courses=[]
    for data in registrations:
        if data.student_id== student_id:
            courses.append(data)
    return courses
            


