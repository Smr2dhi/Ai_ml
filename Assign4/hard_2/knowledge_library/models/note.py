class Note:
    def __init__(self,note_id,title,content,category):
        self.note_id=note_id
        self.title=title
        self.content=content
        self.category=category

    def to_dict(self):
        obj_to_dict={
            "note_id":self.note_id,
            "title":self.title,
            "content":self.content,
            "cateory":self.category

        }
        return obj_to_dict

def note_from_dict(data):
    return Note(
        data["note_id"],
        data["title"],
        data["content"],
        data["category"]
    )
