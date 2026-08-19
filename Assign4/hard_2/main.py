from Assign4.hard_2.knowledge_library.services.note_service import NoteService
from logs.logger import global_logger,session_logger

def main():
    service=NoteService()
    session_logger.info("Knowledge Library session started")

    while True:
        print("\n=== Personal Knowledge Library ===")
        print("1. Add Document")
        print("2. View Documents")
        print("3. Search Documents")
        print("4. Exit")

        choice=input("Enter Choice: ")

        if choice=="1":
            title=input("Title: ")
            content=input("Content: ")
            category=input("Category: ")

            try:
                note=service.add_note(title,content,category)
                print(f"Saved note #{note.note_id}.")
            except ValueError as e:
                print(e)

        elif choice=="2":
            notes=service.list_notes()

            if not notes:
                print("Library is empty.")
            else:
                for note in notes:
                    print(f"[{note.note_id}] {note.title} ({note.category})")
                    print(f"    {note.content}")

        elif choice=="3":
            category=input("Category: ")
            notes=service.search_by_category(category)

            if not notes:
                print("No documents found.")
            else:
                for note in notes:
                    print(note.title)

        elif choice=="4":
            session_logger.info("Knowledge Library session ended")
            print("Goodbye!")
            break

        else:
            global_logger.warning(f"Invalid menu choice: {choice}")
            print("Invalid option")

if __name__=='__main__':
    main()