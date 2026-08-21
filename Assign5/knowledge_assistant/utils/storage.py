import json
import os


file_path = os.path.join(os.path.dirname(__file__), "documents.json")


def load_documents():
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        return json.load(file)


def save_documents(documents):
    with open(file_path, "w") as file:
        json.dump(documents, file, indent=4)