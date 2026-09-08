from fastapi import FastAPI,File,UploadFile,HTTPException
app=FastAPI()
from Assign13.client_api import summarize

@app.post("/summarize")
async def sumarize(file:UploadFile):
    if not file.filename.lower().endswith(".txt"):
            raise HTTPException(
                status_code=400 ,
                detail="Only .txt files are supported")
    
    raw_file= await file.read()
    
    if not raw_file:
        raise HTTPException(
                status_code=400,
                detail="File is empty")
    
    try:
            text=raw_file.decode("utf-8")
    
    except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be valid uTF-8")

    result= await summarize(text)

    return result