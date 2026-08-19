import json
import os

NOTES_FILE=os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "notes.json"
    )
)

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE,"r") as file:
        return json.load(file)

def save_notes(notes):
    with open(NOTES_FILE,"w") as file:
        json.dump(notes,file,indent=4)