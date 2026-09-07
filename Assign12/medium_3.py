import json
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,ValidationError
from Assign12.llmClient import ask_llm,mode
from Assign12.utils import logger

app= FastAPI(title="Policy Extraction API")

class ExtractionRequest(BaseModel):
	document_text:str

class PolicyInfo(BaseModel):
	policy_number: str 
	customer_name: str 
	premium: str 
	coverage_type: str 


MOCK="""{
		"policy_number": "P12345", 
		"customer_name": "John Smith",
		  "premium": "$1200", 
		  "coverage_type": "Automobile"
	}"""

def extract_json_block (text):
	start=text.find("{")
	end=text.rfind("}")

	if start!= -1 and end!= -1:
		return text[start: end+1]
	return text


def build_prompt(document_txt:str)->str:
	return f"""
Task: Extract the insurance policy information from the text below.

use exactly this schema:
{{
    "policy_number": "",
    "customer_name": "",
    "premium": "",
    "coverage_type": ""
}}

Document:{document_txt}
"""

@app.get("/health")
def haalth():
	return{"status":"ok","mode":mode()}


@app.post("/extract_policy",response_model=PolicyInfo)
def create_policy(request: ExtractionRequest):

	prompt=build_prompt(request.document_text)
	response=ask_llm(prompt,mock_response=MOCK)

	logger.info("RESPONSE:%s", response)
	logger.info("TYPE: %s", type(response))

	try:
		data=json.loads(extract_json_block(response))
		return PolicyInfo(**data)

	except (json.JSONDecodeError,ValidationError)as e:
		logger.exception("Exception: %s ",e)
		raise HTTPException(status_code=502, detail="llm returned invalid JSon")


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app,host="127.0.0.1",port=8000)

