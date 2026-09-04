import os
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import(
    Agent,
    Runner,
    set_tracing_disabled,
    set_default_openai_api,
    set_default_openai_client
)
load_dotenv()

log_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"med_3.log"
)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
        format="%(asctime)s -%(filename)s - %(levelname)s - %(message)s"   


)

logger=logging.getLogger(__name__)


api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_ENDPOINT")
model=os.getenv("GEMINI_MODEL")

configured=bool(api_key and base_url and model)
if configured:
    client=AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    set_default_openai_client(client)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


else:
    logger.warning("Env varibales are not set -using mock repsonses")

document = { 
    "name": "Leave Policy", 
    "text": ( 
        "Employees receive 18 days of paid leave per year. " 
        "Unused leave up to 5 days may be carried forward to the next year. " 
        "Leave requests must be submitted at least 3 working days in advance " 
        "through the HR portal. Sick leave requires a medical certificate " 
        "after 2 consecutive days." 
    ), 
} 

ANSWER_TEMPLATE = (
    "Answer the question using ONLY the context below. "
    "If the answer is not in the context, say exactly: "
    "\"I could not find this in the company documents.\"\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)


def check_guardrails(question):

    if not question.strip():
        return False
    
    if len(question)>500:
        return False

    banned={"password","salary of", "confidential"}

    if any(ban in question.lower() for ban in banned):
        return False

    return True

class AIClient():
    def __init__(self):
        self.api_key=api_key
        self.base_url=base_url
        self.model=model

        if configured:
            self.mode="gemini"

            self.agent=Agent(
                name="Ai Assistanta",
                instructions="use only company data to give answer in one sentence",
                model=self.model

            )

        else:
            self.mode="mock"
            self.agent=None

    async def ask(self,question):
        if self.mode=="mock":
            return document["text"].split(".")

        try:

            result=await Runner.run(self.agent,question)

            return result.final_output
        except Exception as e:
            print("llm api failed: ",e)

            logger.error("LLm api failed : %s",e)
            print("Sorry currently unavailable")


async def main():
    client=AIClient()

    while True:

        question=input("Question (q to quit): ")
        if question.lower() == "q":
            print("goodBye!")
            logger.info("Program exited")
            break

    

        if not check_guardrails(question):
            print("Sorry i cannot help with this question")

            logger.warning("Blocked question: %s ",question)
            continue

        prompt= ANSWER_TEMPLATE.format(context=document["text"],question=question)

        answer= await client.ask(prompt)

        print("Answer: ",answer)
        logger.info("Question: %s | Answer: %s",question,answer)


if __name__ == "__main__":
    asyncio.run(main())