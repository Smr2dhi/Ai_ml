from Assign4.knowledge_assistant.app.models.document import Document, document_from_dict
from Assign4.knowledge_assistant.app.utils import storage
from Assign4.knowledge_assistant.app import config


class DocumentService:

    def __init__(self):
        data = storage.load_documents(config.DATA_FILE)

        self.documents = []
        for document in data:
            self.documents.append(
                document_from_dict(document)
            )

    def add_document(self, name, category, tags):
        highest_id = 0

        for document in self.documents:
            if document.document_id > highest_id:
                highest_id = document.document_id

        new_id = highest_id + 1

        document = Document(
            new_id,
            name,
            category,
            tags
        )

        self.documents.append(document)

        storage.save_documents(self.documents)
        return document

    def list_documents(self):
        return self.documents

    def search_by_category(self, category):

        results = []

        for document in self.documents:
            if document.category.lower() == category.lower():
                results.append(document)

        return results

    def search_by_name(self, text):

        results = []

        for document in self.documents:
            if text.lower() in document.name.lower():
                results.append(document)

        return results

    def delete_document(self, document_id):

        for document in self.documents:
            if document.document_id == document_id:
                self.documents.remove(document)

                storage.save_documents(
                    self.documents,
                    config.DATA_FILE
                )

                return True

        return False