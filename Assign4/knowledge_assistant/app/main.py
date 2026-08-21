from Assign4.knowledge_assistant.app import config
from Assign4.knowledge_assistant.app.services.document_service import DocumentService

def display_documents(documents):
    if not documents:
        print("libraray is empty")
        return

    for document in documents:
        print(document.document_id, document.name, document.category, ",".join(document.tags))

def main():
    service =DocumentService()

    while True:
        print(f"===={config.APP_NAME} v{config.VERSION}")
        print("""
                1. Add Document 
                2. View Documents 
                3. Search by Category 
                4. Search by Name 
                5. Delete Document 
                6. Exit 

                """)
        try:
            choice=int(input("Enter your choice: "))

            if choice==1:
                name=input("name: ")
                category=input("category: ")
                raw_tags=input("tags: ")

                tags=[]
                for tag in raw_tags.split(","):
                    tag=tag.strip().lower()

                    if tag:
                        tags.append(tag)

                document = service.add_document(
                    name,
                    category,
                    tags
                )

                print(f"Added document #{document.document_id}.")





            elif choice == 2:
                documents = service.list_documents()
                display_documents(documents)

            elif choice == 3:
                category = input("Category: ")

                documents = service.search_by_category(category)
                display_documents(documents)

            elif choice == 4:
                text = input("Name: ")

                documents = service.search_by_name(text)
                display_documents(documents)

            elif choice == 5:
                document_id = int(input("Document ID: "))

                deleted = service.delete_document(document_id)

                if deleted:
                    print("Document deleted.")
                else:
                    print("Document not found.")

            elif choice == 6:
                print(
                    f"Goodbye from "
                    f"{config.APP_NAME} v{config.VERSION}!"
                )
                break

            else:
                print("Invalid option.")

        except Exception:
            print("Invalid option.")


if __name__ == "__main__":
    main()