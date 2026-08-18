
class DocumentService:
    def __init__(self):
    
        self.documents=[]

    def add_document(self,document):
        self.documents.append(document)
        

    def list_documents(self):
        return self.documents

    def search_by_category(self,category):
        results=[]

        for doc in self.documents:
            if doc.category.lower()==category.lower():
                results.append(doc)
        return results

    