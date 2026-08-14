import json
 
try:
    with open("chat_history.json", "r") as file:
        data = json.load(file)
        print("History loaded successfully")
        print("Message loaded:", len(data))
 
except FileNotFoundError:
    print("No history found - starting a new session-----")
    data = []
 
except json.JSONDecodeError:
    print("File is corrupted - starting a new session----")
    data = []
 
 
while True:
    user = input("Enter the message (q for Quit): ")
 
    if user == "q":
        break
 
    data.append({
        "role": "user",
        "text": user
    })
 
    data.append({
        "role": "assistant",
        "text": f"you said: {user}"
    })
 
    with open("chat_history.json", "w") as file:
        json.dump(data, file, indent=4)
 