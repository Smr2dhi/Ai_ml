from pydantic import Field,BaseModel
from fastapi import FastAPI,HTTPException


# What is the difference between 422 and 400 in this search example?

# Answer:

# 422: Pydantic validation fails → "hi" is too short.(model problem)
# 400: Pydantic validation passes, but our code rejects → "admin" is not allowed.

# HTTP Status Codes — Simple Concept
# 200 OK → Request is valid and successfully processed.
# 400 Bad Request → Request is understood, but your application rejects it because of a business/application rule.
# 422 Unprocessable Entity → Request data fails Pydantic validation before the endpoint logic runs.

# "hi" → 422
# "admin" → 400
# "laptop" → 200


app= FastAPI()

class SearchRequest(BaseModel):
	query:str=Field(min_length=3,max_length=200)

@app.post("/search")
def create_search(request:SearchRequest):

	if request.query.strip() == "":
		raise HTTPException(
			status_code=400,
			detail="Query cannot be blank"
			
		)
	return{
		"query":request.query,
		"results":[],
		"message":"Search executed"

	}