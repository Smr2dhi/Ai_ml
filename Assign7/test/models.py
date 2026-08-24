from pydantic import BaseModel,Field,EmailStr,field_validator

class RegistrationRequest(BaseModel):
    student_id:int=Field(gt=0)
    student_name:str
    course:str
    email:EmailStr

    @field_validator("student_name","course")
    @classmethod
    def not_empty(cls,value):
        if not value.strip():
            raise ValueError("Cannot be empty")
        return value