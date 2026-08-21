import json
from Assign4.knowledge_assistant.app.logs.logger import session_logger, global_logger

def save_documents(documents, file_name):
    try:
        data = []
        for document in documents:
            data.append({
                "document_id": document.document_id,
                "name": document.name,
                "category": document.category,
                "tags": document.tags
            })

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

        session_logger.info(f"Documents saved successfully to {file_name}")

    except OSError as e:
        global_logger.error(f"Error while saving documents: {e}")
        raise

def load_documents(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        global_logger.warning(f"File not found: {file_name}")
        return []

    except json.JSONDecodeError as e:
        global_logger.error(f"JSON decode error in {file_name}: {e}")
        return []