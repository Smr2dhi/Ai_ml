import os
from dotenv import load_dotenv

from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")


if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = AsyncOpenAI(api_key=GEMINI_API_KEY,base_url=GEMINI_ENDPOINT)

model = OpenAIChatCompletionsModel(model=GEMINI_MODEL,openai_client=client)

incident_agent = Agent(
    name="Incident Analyzer",
    instructions="""
        Analyze the user's incident and identify its severity, category, root cause, and recommended action.from provided 
        Keep the response clear, concise, and pointwise in twoo sentences.
        """,
    model=model
    )