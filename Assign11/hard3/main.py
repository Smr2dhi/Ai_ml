from fastapi import FastAPI
from Assign11.hard3.logger import logger
from pydantic import BaseModel
from Assign11.hard3.llm_client import llm_client

app=FastAPI()

documents = [
    {
        "id": 1,
        "name": "Leave Policy",
        "category": "HR",
        "text": "Employees receive 18 days of paid leave per year. Leave requests should be submitted to the manager in advance. Unused leave may be carried forward according to company policy."
    },
    {
        "id": 2,
        "name": "Reimbursement Rules",
        "category": "Finance",
        "text": "Employees can claim reimbursement for approved business expenses. Expense claims must include valid receipts and should be submitted within 30 days. Manager approval is required before reimbursement is processed."
    },
    {
        "id": 3,
        "name": "Company Holidays",
        "category": "HR",
        "text": "The company observes public holidays and selected company holidays each year. The official holiday calendar is shared with employees at the beginning of the year. Employees should check the calendar before planning leave."
    }
]


class AskRequest(BaseModel):
    question:str


def find_matching_documents(question,documents,limit=2):
    logger.info("Searching for matching documents")


    question_words=question.lower().split()
    results=[]

    for doc in documents:
        score=0

        for word in question_words:
            if len(word)>3 and word in doc["text"].lower():
                score+=1

        if score>0:
            results.append((score,doc))

    results.sort(reverse=True)

    final_result=[]
    for score,doc in results[:limit]:
        final_result.append(doc)

    return final_result


def check_guardrails(question):
    blocked_words=[
        "password",
        "secret",
        "api key",
        "credit card",
        "private key"]

    question=question.lower()

    for word in blocked_words:
        if word in question:
            logger.warning("Question blocked by guardrail")
            return False
        
    return True


SYSTEM_PROMPT = (
    "You are the company's AI Knowledge Assistant. "
    "Answer only from the provided context. "
    "If the context does not contain the answer, say exactly: "
    "'I could not find this in the company documents.' "
    "Be concise and professional.")


ANSWER_TEMPLATE = """
Context: 
{context}

Question: 
{question}
"""


@app.post("/ask")
async def ask(request:AskRequest):
    question=request.question

    if not check_guardrails(question):
        logger.warning("Returning blocked response")
        return{
            "question":question,
            "answer":"Sorry, I cannot help with that question.",
            "sources":[],
            "mode":llm_client.mode,
            "total_tokens":0,
            "blocked":True
        }

    matching_documents=find_matching_documents(question,documents,limit=2)

    if not matching_documents:
        logger.info("No matching documents found")
        return{
            "question": question,
            "answer": "I could not find this in the company documents.",
            "sources": [],
            "mode": llm_client.mode,
            "total_tokens": 0
        }

    context=""
    for doc in matching_documents:

        context+="Document: "+doc["name"]+"\n"
        context+=doc["text"]+"\n"

    prompt=ANSWER_TEMPLATE.format(context=context,question=question)
    logger.info("Calling LLM")

    answer,usage=await llm_client.generate_answer(SYSTEM_PROMPT,prompt)

    result=   {
                "question": question,
                "answer": answer,
                "sources": [],
                "mode": llm_client.mode,
                "total_tokens": usage["total_tokens"]
               }

    for doc in matching_documents:
        result["sources"].append(doc["name"])

    return result