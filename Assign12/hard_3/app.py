from fastapi import FastAPI, HTTPException

from Assign12.hard_3.models import DocumentOut, AutoTagResult, AskRequest,StructuredAnswer
from Assign12.hard_3.extractor import ask_for_model

app=FastAPI()


DOCUMENTS = [ 
    {"id": 1, "name": "Remote Work Policy", "category": None, "tags": [], 
     "content": "Employees may work remotely up to three days per week. " 
                "Requests are approved by the reporting manager. Remote employees " 
                "must be reachable during core hours 10:00-16:00."}, 
    {"id": 2, "name": "Expense Reimbursement Guide", "category": None, "tags": [], 
     "content": "Submit expense claims within 30 days with receipts attached. " 
                "Meals during business travel are reimbursed up to a daily cap. " 
                "Approval from the finance team is required."}, 
    {"id": 3, "name": "Python Coding Standards", "category": None, "tags": [], 
     "content": "All backend services use Python 3.11 and follow PEP 8. " 
                "FastAPI is the standard framework. Code review is mandatory " 
                "before merging to main."}, 
] 


def get_tag_mock(doc_id):
    if doc_id == 1:
        return """Here is the JSON you asked for:
    ```json
    {
        "category": "HR",
        "tags": ["remote work", "policy", "approvals"]
    }
    ```"""
    elif doc_id == 2:
        return '{"category": "Finance", "tags": ["expenses", "reimbursement", "receipts"]}'

    elif doc_id == 3:
        return '{"category": "Tech", "tags": ["python", "fastapi", "coding standards"]}'

def get_ask_mock(question):
    question=question.lower()
    if "remote" in question:
        return """{
            "answer": "Employees may work remotely up to three days per week.",
            "sources": ["Remote Work Policy"],
            "confidence": 0.92}"""

    elif "expense" in question or "reimburs" in question:
        return """{
            "answer": "Expense claims must be submitted within 30 days with receipts attached.",
            "sources": ["Expense Reimbursement Guide"],
            "confidence": 0.9}"""

    else:
        return """{
            "answer": "I could not find this in the document library.",
            "sources": [],
            "confidence": 0.2}"""

@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "mock"}




@app.get("/documents", response_model=list[DocumentOut])
def get_documents():
    return DOCUMENTS


@app.post( "/documents/{doc_id}/auto-tag",response_model=DocumentOut)
def auto_tag_document(doc_id:int):
    document=None

    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            document=doc
            break

    if document is None:
        raise HTTPException(status_code=404,detail="Document not found")

    prompt = f"""
            Auto-tag this document.

            Document name:
            {document["name"]}

            Document content:
            {document["content"]}

            Return JSON using this schema:

            {{
                "category": "",
                "tags": []
            }}

            Allowed category values:
            - HR
            - Finance
            - Tech
            - General

            Tag rules:
            - Return 2 to 5 tags.
            - Tags should be short.
            - Tags should be lowercase-ish.
            - Return ONLY valid JSON.
            """

    try:
        result=ask_for_model(prompt,AutoTagResult,get_tag_mock(doc_id))

    except ValueError as e:
        raise HTTPException(status_code=502,detail=str(e))

    document["category"] = result.category
    document["tags"] = result.tags

    return document


@app.post("/ask",response_model=StructuredAnswer)
def ask(request:AskRequest):

    context=""

    for document in DOCUMENTS:
        context+= f"""
            [{document["name"]}]
            {document["content"]}

    """
    prompt = f"""
    Answer the question using only these documents.

    Question:
    {request.question}

    Documents:
    {context}

    Return JSON:

    {{
        "answer": "",
        "sources": [],
        "confidence": 0.0
    }}

    Rules:
    - Answer only from the documents.
    - sources must contain document names from the library.
    - confidence must be between 0 and 1.
    - If the answer is not found, say:
    "I could not find this in the document library."
    - If not found, sources must be empty.
    - Return only JSON.
    """
    try:
        result=ask_for_model(prompt,StructuredAnswer ,get_ask_mock(request.question))
    except ValueError as e:
        raise HTTPException(status_code=502,detail=str(e))

    valid_sources=[]

    for source in result.sources:
        for document in DOCUMENTS:
            if source == document["name"]:
                valid_sources.append(source)

    result.sources=valid_sources
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)