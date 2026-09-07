from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

@app.get("/helath")
def check_health():
	return {"status":"ok" , "service": "practice-api"}

class EchoRequest(BaseModel):
	message:str

class EchoResponse(BaseModel):
	echoed:str
	length:int

@app.post("/echo",response_model=EchoResponse)
def create_echo(request:EchoRequest):
	return {
		"echoed": request.message,
		"length":len(request.message)
	}

@app.get("/")
def welcome():
	return{
		"message": "Welcome to Practice API",
		"availbale_endpoints":["/","/health","/echo"]
	}


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app,host="127.0.0.1",port=8000)

