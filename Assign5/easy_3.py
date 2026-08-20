from fastapi import FastAPI

app=FastAPI()


@app.get("/greet/{name}")
def greet(name):
    return f"Message: Hello,{name}!"


@app.get("/square/{number}")
def square(number:int):
    return f"Square of {number}: {number**2}"

@app.get("/search/")
def query(q: str=""):
    return f"query: {q}, results:[]"



