class Document:
    def __init__(self,document_id,name,category):
        self.document_id=document_id
        self.name=name
        self.category=category

    def to_dict(self):
        document_details={
            "document_id":self.document_id,
            "Name":self.name,
            "Category":self.category 

        }
        return document_details
        
        