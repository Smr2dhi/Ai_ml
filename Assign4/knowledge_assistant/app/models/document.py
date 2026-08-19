class Document:
    def __init__(self, document_id, name, category, tags):
        self.document_id = document_id
        self.name = name
        self.category = category
        self.tags = tags

    def to_dict(self):
        document_details = {
            "document_id": self.document_id,
            "name": self.name,
            "category": self.category,
            "tags": self.tags
        }

        return document_details


def document_from_dict(data):
    return Document(
        data["document_id"],
        data["name"],
        data["category"],
        [tag.lower() for tag in data["tags"]]
    )

