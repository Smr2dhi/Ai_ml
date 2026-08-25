from pydantic import BaseModel,Field,field_validator

class DocumentCreateRequest(BaseModel):
    file_name:str=Field(min_length=1)
    category:str=Field(min_length=1)
    file_size:int=Field(gt=0,le=10485760)

    @field_validator("category")
    @classmethod
    def category_validator(cls,value):
        if value in("HR","Tech","Finance","General"):
            return value
        else:
            raise ValueError("Category must be one of: HR, Tech, Finance, General")

    @field_validator("file_name")
    @classmethod
    def file_name_validator(cls,value):
        if not value.strip():
            raise ValueError("File name cannot be blank")
        return value
        


class DocumentResponse(BaseModel):
    document_id:int
    file_name:str
    category:str
    file_size:int

