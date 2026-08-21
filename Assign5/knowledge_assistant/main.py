from Assign5.knowledge_assistant.utils.storage import load_documents,save_documents
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"app":"knowledge Assistant" ,"version":"0.6"}


@app.get("/health")
def get_home():
    doc=load_documents()
    return{
        "status": "healthy", "documents": len(doc)
    }

try:
    @app.get("/documents")
    def get_documents():
        return load_documents()
    
except FileExistsError as e:
    print("error:",e)

try:
    @app.get("/documents/doc_id")
    def get_doc_id(doc_id:int):

        docs=load_documents()
        for doc in docs:
            if doc.get("id")==doc_id:
                return doc
        return {"error: document not found"}
    
except FileNotFoundError as e:
    print("error:",e)

try:
    @app.post("/documents")
    def create_document(document: dict):
        documents = load_documents()

        if documents:
            new_id = max(doc.get("id", 0) for doc in documents) + 1
        else:
            new_id = 1
        document["id"] = new_id

        if "category" not in document:
            document["category"] = "general"

        if "tags" not in document:
            document["tags"] = []

        documents.append(document)
        save_documents(documents)
        return document
except FileNotFoundError as e:
    print(e)

