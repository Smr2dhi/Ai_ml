from fastapi import FastAPI,UploadFile,File,HTTPException
from pathlib import Path

app=FastAPI()
Path("Assign14/uploads").mkdir(exist_ok=True)

@app.post("/upload/text")
async def create_text(file:UploadFile):

    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400 ,
            detail="Only .txt files are supported")

    raw_file= await file.read()

    if not raw_file:
        raise HTTPException(
            status_code=400,
            detail="File is empty"
                            )

    try:
        text=raw_file.decode("utf-8")

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid uTF-8"
        )

    file_path = Path("Assign14/uploads") / file.filename
    
    with open(file_path,"wb")as f:
        f.write(raw_file)

    return {
        "filename":file.filename,
        "characters":len(text),
        "word":len(text.split()),
        "lines":len(text.splitlines()),
        "preview":text[:200]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)