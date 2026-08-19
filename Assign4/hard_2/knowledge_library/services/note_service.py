from Assign4.hard_2.knowledge_library.models.note import Note,note_from_dict
from Assign4.hard_2.knowledge_library.utils.storage import load_notes,save_notes
from logs.logger import global_logger,session_logger

class NoteService:
    def __init__(self):
        try:
            data=load_notes()
            self.notes=[]

            for note_data in data:
                note=note_from_dict(note_data)
                self.notes.append(note)

            session_logger.info("Notes loaded successfully")

        except Exception:
            global_logger.error("Failed to load notes")
            

    def add_note(self,title,content,category):
        if title.strip()=="":
            global_logger.warning("Attempted to add note with empty title")
            raise ValueError("Title cannot be empty")

        note_id=len(self.notes)+1
        note=Note(note_id,title,content,category)
        self.notes.append(note)

        data=[]
        for note in self.notes:
            data.append(note.to_dict())

        save_notes(data)

        session_logger.info(f"Note #{note_id} added")
        return note

    def list_notes(self):
        session_logger.debug("Listing all notes")
        return self.notes

    def search_by_category(self,category):
        session_logger.debug(f"Searching category: {category}")

        result=[]
        for note in self.notes:
            if note.category.lower()==category.lower():
                result.append(note)

        return result