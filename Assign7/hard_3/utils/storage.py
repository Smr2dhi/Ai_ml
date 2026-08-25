import json

def save_documents(documents,file_name="hard_3.json"):
    
    with open(file_name,"w")as file:
        json.dump(documents,file,indent=4)
        

def load_documents(file_name="hard_3.json"):
    try:
        with open(file_name,"r")as file:
            return json.load(file)
            
    except FileNotFoundError as e:
        print("Error while loading file: ",e)
        return []

    except json.JSONDecodeError as e:
        print("Decode error:",e)
        return []
