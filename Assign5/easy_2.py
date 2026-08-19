from fastapi import FastAPI
from datetime import datetime
app= FastAPI()

@app.get("/")
def fun():
    return{
        "message":"Welcome to the AI Engineering API"
        }

@app.get("/health")
def health():
    return{
        "Status":"helathy"
    }

@app.get("/about")
def about():
     data = {
        "name":"Samriddhi",
        "Version":"0.1"
    }
     return data

now =str(datetime.now())
@app.get("/time")
def time():
    return now