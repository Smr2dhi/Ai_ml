import json

captured_responses = [ 
    '{"name": "John Smith", "email": "john@gmail.com", "phone": "1234567890"}', 
    'Here is the JSON:\n{"name": "John Smith", "email": "john@gmail.com"}', 
    '{"name": "John Smith", "email": "john@gmail.com", "phone": "1234567890",}', 
    '{"name": "John Smith", "email": "john@gmail.com"}', 
] 

required=["name","email","phone"]
usable_reponse=0

for index ,response in enumerate(captured_responses,start=1):
	
    try:
        data=json.loads(response)

        missing_field=[f for f in required if f not in data]

        if missing_field:
            print(f"Response {index}: Missing Fields: {missing_field}")

        else:
            print(f"Response{index}: OK")
            usable_reponse+=1

    except json.JSONDecodeError as e:
        print(f" Response {index}: Invalid json->",e)
print(f"Usable responses:{usable_reponse} of {len(captured_responses)}")