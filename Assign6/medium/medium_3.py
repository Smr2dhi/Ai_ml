from pydantic import BaseModel
from fastapi import FastAPI


app=FastAPI()

class SearchRequest(BaseModel):
	query:str
	category:str |None=None
	limit:int | None= None

class SearchResponse(BaseModel):
	results:list
	total_count:int
	



documents = [ 
    {"id": 1, "name": "HR Leave Policy",   "category": "HR"}, 
    {"id": 2, "name": "Remote Work Policy", "category": "HR"}, 
    {"id": 3, "name": "Python Style Guide", "category": "Tech"}, 
    {"id": 4, "name": "API Design Guide",   "category": "Tech"}, 
] 

@app.post("/search", response_model=SearchResponse)
def create_search(search:SearchRequest):
	results=[]

	for data in documents:
		query_match=search.query.lower() in data["name"].lower()
		category_match= (search.category is  None or search.category.lower() in data["category"].lower())

		if query_match and category_match:
			results.append(data)


	if search.limit is not None:
		results=results[:search.limit]

	return{
			"results":results,
			"total_count":len(results),

				}
	 