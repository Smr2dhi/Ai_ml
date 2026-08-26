from Assign7.hard_3.services.document_service import DocumentService
from Assign7.hard_3.models.document import DocumentCreateRequest,DocumentResponse
from Assign7.hard_3.utils.logging import logger
from fastapi import FastAPI,HTTPException


app=FastAPI()

document_obj=DocumentService()

@app.get("/documents",response_model=list[DocumentResponse])
def get_document(category:str=None):


    documents=document_obj.get_all(category)

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    logger.warning("No document found")
    return documents

@app.get("/documents/{document_id}",response_model=DocumentResponse)
def get_documents_by_id(document_id:int):

    document=document_obj.get_by_id(document_id)

    if document :
        return document

    else:
        logger.warning("No student found")
        raise HTTPException(
            status_code=404,
            detail="missing id"
        )

@app.post("/documents",response_model=DocumentResponse)
def create_document(request:DocumentCreateRequest):

            
    document=document_obj.create(
        request.file_name,
        request.category,
        request.file_size
    )
    logger.info("studenst created")
    return document


@app.put("/documents/{document_id}")
def update_document(document_id:int,request:DocumentCreateRequest):

    document =document_obj.update(
        document_id,
        request.file_name,
        request.category,
        request.file_size
    )
    logger.info("studenst updated")

    if not document:
        logger.warning("No student found")
        raise HTTPException(
            status_code=404,
            detail="No such document exists to update"
        ) 
    return document

@app.delete("/documents/{document_id}")
def delete_document(document_id:int):
    document=document_obj.delete(document_id)

    if not document:
        logger.warning("No student found")
        raise HTTPException(
            status_code=404,
            detail="No such documnets exists"
        )
    logger.warning("student found")
    return document