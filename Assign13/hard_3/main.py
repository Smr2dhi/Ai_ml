from fastapi import FastAPI,UploadFile,File,HTTPException 
from pydantic import BaseModel
from datetime import datetime, timezone
from Assign13 import ai_client
impot logging

log_path=os.join(os.path.dirname(__file__),"app.log")

logging.basicConfig(
    filename="log_path",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app=FastAPI(title="AI Knowledge Assistant",description="This is a semantic search engine that uses AI to provide answers to your questions based on the documents you provide.",version="1.0.0")

next_id=1

library=[]
class Document(BaseModel):
    title:str
    content:str

def public_view(doc):
    return {
        "id":doc["id"],
        "filename":doc["filename"],
        "size_byte":doc["size_byte"],
        "uploaded_at":doc["uploaded_at"],
        "summary":doc["summary"],
        "key_points":doc["key_points"],
        "action_items":doc["action_items"],
    }

@app.post("/documents/upload")
async def create_document(file:UploadFile=File(...)):
    global next_id

    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400,detail="Invalid file type. Only .txt files are allowed.")
    
    raw_content=await file.read()

    if len(raw_content)==0:
        raise HTTPException(status_code=400,detail="Uploaded file is empty.")
    
    if len(raw_content)>1*1024*1024:
        raise HTTPException(status_code=413,detail="Uploaded file exceeds the 1MB size limit.")

    try:
        content=raw_content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400,detail="Invalid file content. Only valid UTF-8 encoded text files are allowed.")


    logger.info(f"Document '{file.filename}' uploaded successfully.")

    summary_data=await ai_client.summarize(content)
    embedding=ai_client.get_document_embedding(content)

    
    doc=({
        "id":next_id,
        "filename":file.filename,
        "size_byte":len(raw_content),
        "uploaded_at":datetime.now(timezone.utc).isoformat(),
        "content": content,
        "summary":summary_data["summary"],
        "key_points":summary_data["key_points"],
        "action_items":summary_data["action_items"],
        "embedding":embedding
    })

    library.append(doc)
    next_id += 1
    return public_view(doc)


@app.get("/documents")
async def list_documnets():
    return{
        "total_documents":len(library),
        "documents":[public_view(doc) for doc in library]
    }

@app.get("/documents/{doc_id}")
async def get_document(doc_id:int):
    for doc in library:
        if doc["id"] == doc_id:
            return public_view(doc)
    raise HTTPException(status_code=404, detail="Document not found")

@app.get("/search/semantic")
async def semantic_search(query:str, top_k:int=3):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required.")

    if not library:
        return {
            "query": query,
            "results": [],
            "mode":ai_client.get_mode(),
        }

    embedding=ai_client.get_query_embedding(query)

    scored=[]
    for doc in library:
        score=ai_client.cosine_similarity(
            embedding,
            doc["embedding"]
        )
        print("Document:",doc["filename"])
        print("Score:",score)
        scored.append((score,doc))

    scored.sort(key=lambda x:x[0],reverse=True)

    results=[]
    for score,doc in scored[:top_k]:
        results.append({
            "id":doc["id"],
            "filename":doc["filename"],
            "score":round(score,3),
            "summary":doc["summary"],
        })

    return{
        "query":query,
        "mode":ai_client.get_mode(),
        "results":results
    }