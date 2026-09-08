from fastapi import FastAPI,File,UploadFile,HTTPException
import logging
import uuid
import time
from pathlib import Path
from Assign13.client_api import summarize

app=FastAPI()

import logging
import os

log_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "app.log"
)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)

logger=logging.getLogger(__name__)

upload_dir=Path("uploads")
upload_dir.mkdir(exist_ok=True)

MAX_FILE_SIZE=1*1024*1024

@app.post("/summarize")
async def create_summary(file:UploadFile):
    started = time.perf_counter()

    if not file.filename or not file.filename.lower().endswith(".txt"):

        logger.warning("Rejected uploaded file invalid type :%s needed .txt file",file.filename)
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported."
        )

    raw=await file.read()
    if len(raw)==0:
        logger.warning("Rejected upload (empty file): %s", file.filename)

        raise HTTPException(
            status_code=400,
            detail="File is empty"
        )

    if len(raw)>MAX_FILE_SIZE:
          logger.warning("Rejected upload (too large): %s (%d bytes)",file.filename,len(raw))

          raise HTTPException(
               status_code=413,
               detail="File larger than 1 MB"
          )

    try:
         content=raw.decode("utf-8")

    except UnicodeDecodeError:
         logger.warning("Rejected upload (not UTF-8): %s", file.filename)
         raise HTTPException(status_code=400, detail="File is not valid UTF-8 text.") 

    store_as=uuid.uuid4().hex[:8] + "_"+file.filename
    (upload_dir/store_as).write_text(content,encoding="utf-8")

    result= await summarize(content)
    duration_ms=round((time.perf_counter()-started)*1000)

    return{
         "filename": file.filename, 
        "stored_as": store_as, 
        "size_bytes": len(raw), 
        "summary": result.get("summary", ""), 
        "key_points": result.get("key_points", []), 
        "action_items": result.get("action_items", []),  
        "duration_ms": duration_ms, 

    }

