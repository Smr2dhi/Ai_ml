from dotenv import load_dotenv
from openai import AsyncOpenAI
import time

from agents import(
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled
)
import logging
import os
set_tracing_disabled(True)

log_file=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"med_2.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger=logging.getLogger(__name__)


class AIClient():
    def __init__(self):
        load_dotenv()
        self.api_key=os.getenv("GEMINI_API_KEY")
        self.endpoint=os.getenv("GEMINI_ENDPOINT")
        self.model=os.getenv("GEMINI_MODEL")

        if self.api_key and self.endpoint:
            self.mode="Gemini-openai"

            self.client=AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.endpoint
            )

            set_default_openai_client(self.client)
            set_default_openai_api("chat_completions")

            self.agent = Agent(
            name="AI Assistant",
            instructions="You are a helpful assistant. Answer in one sentence.",
            model=OpenAIChatCompletionsModel(
            model=self.model,
            client=self.client
    )
)

        else:
            self.mode="mock"
            self.client=None
            logging.warning("Printing mock responses---,not configed")
            print("[NOTICE] invalid config using mock responses ")


system_prompt="You are a helpful assistant. answer in one sentence "


async def generate_reponse(self,user_prompt,system_prompt):
    if self.mode=="mock":
        return "Mock result"+user_prompt

    for attempt in range(2):
        try:
            
            result=await Runner.run(self.agent,user_prompt)

            return result.final_output

        except Exception as e:
            print("LLM api call failed: ",e)

            if attempt==0:
                time.sleep(2)

    logger.warning("Sorry llm out of service.please try later")
    return"Sorry LLm is out of service"
