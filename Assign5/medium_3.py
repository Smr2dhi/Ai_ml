from fastapi import FastAPI

app=FastAPI()

students = [ 
    {"id": 101, "name": "John",  "marks": 75, "city": "Delhi"}, 
    {"id": 102, "name": "Sara",  "marks": 92, "city": "Mumbai"}, 
    {"id": 103, "name": "Mike",  "marks": 38, "city": "Delhi"}, 
    {"id": 104, "name": "Priya", "marks": 85, "city": "Chennai"}, 
] 

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/students")
def student():
    return students


@app.get("/students/search")
def search(name:str="" , city:str=""):
    results=[]

    for std in students:
        if std["name"].lower()==name.lower() and std["city"].lower()==city.lower():

            results.append(std)
    return {
            "count":len(results),
            "results":results
            }


@app.get("/students/stats")
def stats():
    topper=students[0]
    total_students=len(students)
    pass_students=0
    total_marks=0
    
    for i in students:
        total_marks+=i["marks"]

        if i["marks"]>=40:
            pass_students+=1

        if i["marks"]>topper["marks"]:
            topper=i
        
    average_marks=total_marks/total_students
    pass_percentage=(pass_students/total_students)*100
       
    return{
        "total":total_students,
        "average_marks":average_marks,
        "topper":topper["name"],
        "pass_percentage":pass_percentage

    }


@app.get("/students/count")
def count():
    return len(students)



    


@app.get("/students/{student_id}")
def student_id_func(student_id:int):
    for i in students:
        if i["id"]==student_id:
            return i
        
    return "Error: Student not found"