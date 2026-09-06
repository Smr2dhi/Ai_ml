from typing import Literal
from pydantic import BaseModel
from Assign12.llmClient import ask_llm
import json

class TicketClassfication(BaseModel):
	ticket_type:Literal["billing","technical","account","general"]
	priority:Literal["low","medium","high"]

	reason:str

ticket_text= "I was charged twice this month and I want a refund immediately!" 


prompt="""
you are a ticket classifictaion assistant
use given instruction  carefully:
1.return only json.do not include expalanation or any extra
2. use this exact schema {
"ticket_type": "",
"priority": ""
}
3. allow values for ticket type:["billing", "technical", "account", "general"]

4. allowed values for priority ["low", "medium", "high"]
Ticket:{ticket_text}
"""	

response=ask_llm(prompt)
data=json.loads(response)

validated=TicketClassfication(**data)
print("---Ticket Classified---")
print(f"Type: {validated.ticket_type}")
