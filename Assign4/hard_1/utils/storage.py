import json

def save_students(students,file_name):
    
    with open(file_name,"w")as file:
        json.dump(students,file,indent=4)
        

def load_students(file_name):
    try:
        with open(file_name,"r")as file:
            return json.load(file)
            
    except FileNotFoundError as e:
        print("Error while loading file: ",e)
        return []

    except json.JSONDecodeError as e:
        print("Decode error:",e)
        return []
