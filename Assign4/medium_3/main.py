from .models.document import Document
from .services.document_service import DocumentService
from ..medium_2.utils.storage import save_documents,load_documents

service =DocumentService()
service.add_document(Document(1,"HR Policy","HR"))
service.add_document(Document(2,"leave Policy","HR"))
service.add_document(Document(3,"Pyton Guide","Tech"))

print("---All Documents----")

for doc in service.list_documents():
    print(f"[{doc.document_id}] {doc.name} ({doc.category})")

search=input("enter the category to search..")
print(f"---Search:{search}")
results=service.search_by_category(search)

for doc in results:
    print(doc.name)

Doc_list= []
for doc in service.list_documents():
    Doc_list.append(doc.to_dict())

save_documents(Doc_list,"Assign4/Medium_3/documents.json")
print ("Documet saved")

