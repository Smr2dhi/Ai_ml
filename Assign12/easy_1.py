import json
from Assign12.llmClient import ask_llm,mode

input_text="""
Customer Priya Nair reported the issue. She can be reached at
priya.nair@example.com or on 9876501234.
"""
prompt=f"""
Task: Extract the customer's contact details from the text below.
Return JSON only

use exactly this schema:
{{"name": "", "email": "", "phone": ""}}

Input:{input_text}
"""

mock_response = '{"name": "Priya Nair", "email": "priya.nair@example.com", "phone": "9876501234"}'


response=ask_llm(prompt,mock_response=mock_response)

data=json.loads(response)

print("---Extracted contact----")

print("Name:",data["name"])
print("Email:",data["Email"])
print("Phone:",data["Phone"])

print(f"(mode:{mode()})")

