from pydantic import BaseModel

from fastapi import FastAPI
from typing import Optional

app=FastAPI()

class UploadInfo(BaseModel):
	uploaded_by:str
	department:Optional[str]=None

class DocumentCreate(BaseModel):
	name:str
	category:str
	tags:list
	uploader:UploadInfo

class DocumentResponse(BaseModel):
	document_id:int
	name:str
	category:str
	tags:list
	uploader:UploadInfo

class DocumentListResponse(BaseModel):
	documents:list
	total:int

class SearchResponse(BaseModel):
	results:list
	total_count:int

class LibrarySummary(BaseModel):
	total_documents:int
	total_categories:int
	categories:list
	unique_tags:list
	top_category:Optional[str]=None

library=[
	{
		"document_id":1,
  		"name": "HR Leave Policy", 
        "category": "HR", 
        "tags": ["leave", "policy"], 
        "uploader": {"uploaded_by": "john", "department": "HR"}, 
	},

	{ "document_id": 2, 
        "name": "Python Style Guide", 
        "category": "Tech", 
        "tags": ["python", "style"], 
        "uploader": {"uploaded_by": "sara", "department": None}, 
    },
]


@app.get("/documents",response_model=DocumentListResponse)
def get_documents():

	return {
		"documents":library,
		"total":len(library)
		}

@app.post("/documents",response_model=DocumentResponse)
def add_documents(document:DocumentCreate):
	doc_id=len(library)+1

	document_data=document.model_dump()
	document_data["document_id"]=doc_id

	library.append(document_data)

	return document_data

	


@app.get("/documents/{document_id}",response_model=DocumentResponse)
def get_id(document_id:int):

	for doc in library:
		if doc["document_id"] == document_id:
			return doc


@app.get("/search",response_model=SearchResponse)
def search_document(query:str,category:Optional[str]=None):
	results=[]

	for doc in library:
		if query.lower() in doc["name"].lower():
			if category is None or doc["category"].lower()==category.lower():
				results.append(doc)

	return{
		"results":results,
			"total_count":len(results)
	}

@app.get("/summary",response_model=LibrarySummary)
def summary():
	categories=[]
	unique_tags=set()
	category_count={}

	for doc in library:
		category=doc["category"]

		if category not in categories:
			categories.append(category)

		unique_tags.update(doc["tags"])

		if category in category_count:
			category_count[category]+=1

		else:
			category_count[category]=1

		top_category=None
		top_count=0

		for category in category_count:
			
			if category_count[category]>top_count:
				top_count=category_count[category]
				top_category=category

		return{
			 "total_documents": len(library),
        	"total_categories": len(categories),
        	"categories": sorted(categories),
        	"unique_tags": sorted(unique_tags),
        	"top_category": top_category

		}
	


	
	