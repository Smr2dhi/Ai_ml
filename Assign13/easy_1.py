from fastapi import FastAPI, UploadFile, File,HTTPException

app = FastAPI()

MAX_FILE_SIZE =1*1024*1024

@app.post("/upload/inspect")
async def upload_file(file: UploadFile):

    if file.size >MAX_FILE_SIZE:
        raise HTTPException(status_code=413,detail="File too lare.max file size is 1 MB")

    content =  await file.read()

    text=content.decode("utf-8")

   

    return {
        "message": "File uploaded successfully",
        "content": text,
        "content_type": file.content_type,
        "size": len(content)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)