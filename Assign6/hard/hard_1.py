from pydantic import BaseModel,Field
from fastapi import FastAPI
from typing import Optional


app= FastAPI()
students_list=[]
class Address(BaseModel):
	city:str
	country:str="India"

class StudentCreateRequest(BaseModel):
	name:str
	email:str
	branch:str
	year:int=Field(gt=0)
	address:Address
	phone:Optional[str]=None


class StudentResponse(BaseModel):
	student_id:int
	name:str
	branch:str
	year:int
	address:Address

class StudentListResponse(BaseModel):
	student:list
	total:int


@app.post("/students",response_model=StudentResponse)

def add_students(student:StudentCreateRequest):
	student_id=len(students_list)+1
	

	student_dict={
		"student_id":student_id,
		"name":student.name,
		"branch":student.branch,
		"year":student.year,
		"address":student.address
	}
	students_list.append(student_dict)
	return student_dict
	 
	
@app.get("/students",response_model=StudentListResponse)
def get_students():
	return {
		"student":students_list,
		"total":len(students_list)
	}

@app.get("/students/{student_id}",response_model=StudentResponse)
def get_student_byId(student_id:int):
	for std in students_list:
		if std["student_id"]==student_id:
			return std

@app.put("/students/{student_id}",response_model=StudentResponse)
def get_address(student_id:int,address:Address):
	for std in students_list:
		if std["student_id"]==student_id:
			std["address"]=address

			return {
				"student_id":std["student_id"],
				"name":std["name"],
				"branch":std["branch"],
				"year":std["year"],
				"address":std["address"]

			}