from Assign7.hard_3.utils.storage import load_documents,save_documents
from Assign7.hard_3.utils.logging import logger

class DocumentService:
    def __init__(self):
        self.documents=load_documents()
        if self.documents:
            self.document_id=max(doc["document_id"] for doc in self.documents)+1

        else:
            self.document_id=1

    def get_all(self,category=None):

        if category:
            return[
                document 
                for document in self.documents
                  if document["category"]==category
                  ]
        logger.info("Student found")
        return self.documents

    def get_by_id(self,document_id):
        for data in self.documents:
            if data["document_id"]==document_id:
                return data

        logger.warning("No student found")
        return None

    def create(self,file_name,category,file_size):
        document={
            "document_id":self.document_id,
            "file_name":file_name,
            "category":category,
            "file_size":file_size,

        }
        self.documents.append(document)
        save_documents(self.documents)
        logger.info("Stuent cretaed---")

        self.document_id+=1

        return document

    def update(self,document_id,file_name,category,file_size):
        document=self.get_by_id(document_id)

        if not document:
            logger.warning("No student found")
            return None
        
        document["file_name"]= file_name
        document["category"]=category
        document["file_size"]=file_size

        save_documents(self.documents)
        logger.info("Stuent updated---")
        return document

    def delete(self,document_id):
        document=self.get_by_id(document_id)

        if not document :
            logger.warning("No student found")
            return None
        
        self.documents.remove(document)

        save_documents(self.documents)

        return {
            "message":f"document deleted {document_id}"
        }

    
