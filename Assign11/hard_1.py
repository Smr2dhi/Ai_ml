from Assign11.medium_2.ai_client import AIClient, generate_reponse
import os 
import logging
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from openai import APIConnectionError, RateLimitError, APIError
log_file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"hard_1.log"
)

logging.basicConfig(
    filename=log_file,
        level=logging.INFO,
        format="%(asctime)s -%(filename)s - %(levelname)s - %(message)s"   

)

logger=logging.getLogger(__name__)

load_dotenv()

personas={
     "1": ("Helpful assistant", "You are a helpful AI assistant."),
    "2": ("Career counselor", "You are a career counselor."),
    "3": ("Company knowledge assistant", "You are a company knowledge assistant.")

}

def log_conversation(question,answer):
    try:
        with open("Conversation_log.txt","w")as file:
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{time}] USER: {question}\n")

            file.write(f"[{time}] Assistant: {answer}\n")

            logger.info("Converstaion saved")

    except Exception as e:
        logger.error("Fialed conversation log file :%s",e)

def log_error(error):
    try:
        with open("error_log.txt","w")as file:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{time}] ERROR: {error}\n")

        logger.error("Error saved :%s",error)

    except Exception as e:
         logger.error("Error log failed: %s", e)


async def main():
    print("""

                === Mini AI Assistant === 
                Choose a persona: 
                1. Helpful assistant 
                2. Career counselor 
                3. Company knowledge assistant
                4. exit
                """)

    choice = input("Persona: ").strip()

    while choice not in personas:
        print("Invalid choice")
        choice = input("Persona: ").strip()

    system_prompt = personas[choice][1]

    client = AIClient()

    questions = 0
    errors = 0

    while True:

        question = input("Enter your input: ").strip()

        if question.lower() == "exit" or question.lower() == "quit":
            break

        if question == "":
            continue
            questions += 1

        try:
            answer = await generate_reponse(
            client,
            question,
            system_prompt
        )
        except APIConnectionError as e:
            print(f"Connection error: {e}")
            errors += 1
            log_error(e)
            continue

        except RateLimitError as e:
            print(f"Rate limit error: {e}")
            errors += 1
            log_error(e)
            continue

        except APIError as e:
            print(f"API error: {e}")
            errors += 1
            log_error(e)
            continue

        except Exception as e:
            print(f"Unexpected error: {e}")
            errors += 1
            log_error(e)
            continue

        print("Assistant:", answer)

        log_conversation(question, answer)

       

    print("\n--- Session Summary ---")
    print("Questions asked :", questions)
    print("Errors          :", errors)
    print("Mode            :", client.mode)
    print("Conversation log: conversation_log.txt")
    print("Error log       : error_log.txt")




if __name__ == "__main__":
    asyncio.run(main())