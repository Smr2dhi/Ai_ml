import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)


class LLMClient:

    def __init__(self):

        load_dotenv()

        set_tracing_disabled(True)

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = os.getenv("GEMINI_ENDPOINT")
        self.model_name = os.getenv("GEMINI_MODEL")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        self.model = OpenAIChatCompletionsModel(
            model=self.model_name,
            openai_client=self.client
        )

    async def llm_call(
        self,
        prompt,
        system_instruction=""
    ):

        agent = Agent(
            name="Assistant",
            model=self.model,
            instructions=system_instruction
        )

        result = await Runner.run(
            agent,
            prompt
        )

        return result.final_output