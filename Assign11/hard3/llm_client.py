from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import asyncio
from Assign11.hard3.logger import logger

from agents import (
    Agent,
    Runner,
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled
)



class LLMClient():
    def __init__(self):
        load_dotenv()

        self.api_key=os.getenv("GEMINI_API_KEY")
        self.base_url=os.getenv("GEMINI_ENDPOINT")
        self.model=os.getenv("GEMINI_MODEL")
        self.llm_version=os.getenv("DEFAULT_API_VERSION")

        self.last_error=None

        print("API KEY loaded:", bool(self.api_key))
        print("ENDPOINT loaded:", bool(self.base_url))
        print("MODEL loaded:", bool(self.model))

        if self.api_key and self.base_url :
            self.mode="GEMINI -Model"
            self.client=AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            set_default_openai_client(self.client)
            set_default_openai_api("chat_completions")
            set_tracing_disabled(True)

        else:
            self.mode="mock"
            self.client=None

    def mock_response(self):
        print("[NOTICE] Gemini env vars are not set-using mock responses")
        print("ZERO_USAGE = prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 ")

        return "Employees receive 18 days of paid leave per year.", {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }


    async def generate_answer(self,system_prompt,user_prompt):
        if self.mode=="mock":
            return self.mock_response()

        try:
            logger.info("Calling Gemini API")

            agent=Agent(
                name="AI assistant knowledge",
                instructions=system_prompt,
                model=self.model
            )

            result=await Runner.run(agent,user_prompt)

            answer=result.final_output
            usage=result.context_wrapper.usage

            usage_data={
                "prompt_tokens":usage.input_tokens,
                "completion_tokens":usage.output_tokens,
                "total_tokens":usage.total_tokens
            }

            return answer,usage_data
        except Exception as e:
            self.last_error=str(e)
            print("Sorry, the AI service is currently unavailable. Please try again later.")
            logger.exception("LLM API error")
            return self.mock_response()


llm_client=LLMClient()