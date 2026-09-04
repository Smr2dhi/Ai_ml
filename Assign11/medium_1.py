from dotenv import load_dotenv
import os
import asyncio
import logging

from openai import AsyncOpenAI
from agents import (
    Agent,Runner,
set_default_openai_api,
set_default_openai_client,
set_tracing_disabled)

load_dotenv()
set_tracing_disabled(True)


log_file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"med_1.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger= logging.getLogger(__name__)


def mock_response(user_prompt):
    if user_prompt.startswith("Summarize"):
        return "Point 1 \n Point-2 \n Point-3"

    if user_prompt.startswith("Classify"):
        return "Complaints"

    if user_prompt.startswith("Exract"):
        return '{"name":"Sam", "email":"sam@gmail.com"}'

    if user_prompt.startswith("Generate"):
        return("1.How much leave do I get?\n2. Can leave carry forward?\n" 
                "3. How do I apply?\n4. What about sick leave?\n" 
                "5. Who approves leave?")

    logging.error("mock response ")
    return "Mock response nothing matched ---"


    

async def run_task(system_prompt,user_prompt):
    api_key =os.getenv("GEMINI_API_KEY")
    end_point=os.getenv("GEMINI_ENDPOINT")
    model=os.getenv("GEMINI_MODEL")

    if not api_key or not end_point:
        logger.warning("not configed ")
        print("[NOTICE] OPENAI env vars are not set-using mock responses")

        logger.info("returning mock responses")
        return mock_response(user_prompt)

    try:
        logger.info("Calling real llm")
        client=AsyncOpenAI(
            api_key=api_key,
            base_url=end_point

        )
        set_default_openai_client(client)
        set_default_openai_api("chat_completions")

        agent=Agent(
            name="Gemini agent",
            instructions=system_prompt,
            model=model

        )

        result=await Runner.run(agent,user_prompt)

        usage=result.context_wrapper.usage
        print("Requests: ",usage.requests)
        logger.info(f"Requests: {usage.requests}")

        print("Input tokens: ",usage.input_tokens)
        logger.info(f"Input tokens: {usage.input_tokens}")

        print("Output tokens:", usage.output_tokens)
        logger.info(f"Output tokens: {usage.output_tokens}")

        print("Total tokens:", usage.total_tokens)
        logger.info(f"Total tokens: {usage.total_tokens}")

        return result.final_output

    except Exception as e:
        print("[Error]",e)

        print("Using mock resonses")
        logger.info("returning mock responses")
        return mock_response(user_prompt)


async def main():
    system_prompt=("Act as a assistant . Follow the instruction carefully")

    while True:
        print("""
            === LLM Task Switchboard === 
            1. Summarize text 
            2. Classify a message 
            3. Extract contact info (JSON) 
            4. Generate FAQs 
            5. Exit 

""")

        try:
            choice=input("Choice: ").strip()

            if choice=="1":
                text=input("Text to summarize: ")
                user_prompt=("Summarize the following txt in 3 bullet:\n"+text)

                result=await run_task(system_prompt,user_prompt)
                print("Result: ",result)

            elif choice=="2":
                text=input("Text to clasify the message")
                user_prompt=("Classify this message as Complaint,Inquiry, or Feedback.Reply with one word :\n"+text)

                result=await run_task(system_prompt,user_prompt)
                print("Result: ",result)

            elif choice=="3":
                text=input("text containing contact info:")
                user_prompt=("Extract name and email from text. Return json only "+text)

                result= await run_task(system_prompt,user_prompt)

            elif choice=="4":
                text=input("topics: ")
                user_prompt=("Generate 5 FAQs about the topic:\n"+text)

                result=await run_task(system_prompt,user_prompt)
                print("Result: ",result)

            elif choice=="5":
                custom_input=input("enter system prompt: ")
                user_prompt=input("enter user prompt: ")

                result=await run_task(custom_input,user_prompt)
                print("result: ",result)

            elif choice=="6":
                print("----Exit----")
                logger.info("Exit")
                break

            else: 
                logger.warning("Invalid option")
                print("Invalid option")

        
        except Exception as e:
            print("Error---",e)
            logger.error("Exception : %s",e,exc_info=True)



if __name__=="__main__":
    asyncio.run(main())