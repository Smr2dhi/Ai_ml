from pydantic import BaseModel,ValidationError
from fastapi import FastAPI,HTTPException
from typing import Literal
from Assign12.utils import logger
import json

class TicketRequest(BaseModel): 
    text: str 
 
class TicketClassification(BaseModel): 
    ticket_type: Literal["billing", "technical", "account", "general"] 
    priority: Literal["low", "medium", "high"] 
    summary: str 

def extract_json_block(text):
    start=text.find("{")
    end=text.rfind("}")

    if start == -1 or end == -1:
        return text
    return text[start:end+1]

        

def classify_with_retry(prompt,mock_response,max_attempts=3):

    for attempt in range(max_attempts):

        try:
            json_text=extract_json_block(mock_response)
            data=json.loads(json_text)

            result=TicketClassification(**data)
            logger.info(f"Attempt {attempt+1} : sucessful")
            return result
        except (json.JSONDecodeError,ValidationError):

            logger.error(f" Attempt {attempt+1} : Failed")

            prompt=prompt+"Return only valid json"

    raise ValueError("Classification failed after all attempts")

def mock_classifiaction(text):
    text=text.lower()
    if "refund" in text or "charged" in text:
        return '{"ticket_type": "general", ' \
        '"priority": "low", ' \
        '"summary": "User has a general support request."}'

    elif "password" in text or "login" in text:
        return """```json
            {
                "ticket_type": "account",
                "priority": "medium",
                "summary": "User cannot log in and needs a password reset."
            }
            ```"""
    elif "error" in text or "crash" in text:
        return '{"ticket_type": "technical", "priority": "high", "summary": "User reports an application error."}'

    else:
        return '{"ticket_type": "general", "priority": "low", "summary": "User has a general support request."}'

app=FastAPI()
classifications = []


@app.post("/tickets/classify",response_model=TicketClassification)
def classify_ticket(ticket:TicketRequest):
    prompt=f"""
            Classify this support ticket.

        Return only JSON.

        Ticket:
        {ticket.text}
"""
    mock_response= mock_classifiaction(ticket.text)
    try:
        result=classify_with_retry(prompt,mock_response)
        classifications.append(result)

        logger.info("Ticket lasification sucsesful")
        return result
    except Exception as e:
        raise HTTPException (status_code=502,detail=str(e))


@app.get("/tickets/stats")
def ticket_stats():

    priority_counts = {}
    type_counts = {}

    for ticket in classifications:
        priority = ticket.priority
        ticket_type = ticket.ticket_type

        priority_counts[priority]=(priority_counts.get(priority,0)+1)
        type_counts[ticket_type]=( type_counts.get(ticket_type, 0) + 1)

    logger.info("Ticket statistics requested")

    return{
        "total": len(classifications),
        "by_priority": priority_counts,
        "by_type": type_counts

        }

@app.get("/health")
def health():
    return {
        "status":"ok",
        "mode":"mock"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
