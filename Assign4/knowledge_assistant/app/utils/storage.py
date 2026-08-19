import json


from logs.logger import session_logger,global_logger


def save_students(students,file_name):

    try:
        with open(file_name,"w")as file:
            json.dump(students,file,indent=4)

            session_logger.info(f"Students saved successfully to {file_name}")

    except OSError as e:
        global_logger.error(f"Error while saving student {e}")
        raise

def load_students(file_name):
    try:
        with open(file_name,"r")as file:
            return json.load(file)
            
    except FileNotFoundError as e:
        global_logger.warning(f"Error while loading file: {file_name}")
        return []

    except json.JSONDecodeError as e:
        global_logger.error(f"JSON decode error in {file_name}: {e}")
        return []