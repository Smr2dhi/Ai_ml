import json
import os
from Assign13.looger import logger
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled,OpenAIChatCompletionsModel

set_tracing_disabled(True)

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


load_dotenv(ENV_FILE)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

logger.info(
    "GEMINI_API_KEY exists: %s",
    bool(GEMINI_API_KEY)
)
logger.info("GEMINI_ENDPOINT exists: %s", bool(GEMINI_ENDPOINT))
logger.info("GEMINI_MODEL exists: %s", bool(GEMINI_MODEL))


def is_configured():
    return all([GEMINI_API_KEY,
        GEMINI_ENDPOINT,
        GEMINI_MODEL])

logger.info("is_configured: %s", is_configured())
MOCK_MODE =not is_configured()

def get_mode():
    return "mock" if MOCK_MODE else "gemini"

if not MOCK_MODE:
    logger.info("Creating AsyncOpenAI client...")

    client=AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url=GEMINI_ENDPOINT)
    
    logger.info("AsyncOpenAI client created")

    model=OpenAIChatCompletionsModel(
        model=GEMINI_MODEL,
        openai_client=client
    )
    logger.info("Gemini model object created")

    agent=Agent(
        name="Document summarizer",
        instructions="""
        Summarize the given document.
         You are a document summarization assistant.

        Return ONLY valid JSON.

        The JSON must contain exactly these keys:

        {
            "summary": "...",
            "key_points": ["..."],
            "action_items": ["..."]
        }

        Do not return markdown.
        Do not return ```json.
        Do not add any text outside the JSON.
        """
        ,
        model=model
        
    )
    logger.info("Agent created")

async def summarize(text):
    if MOCK_MODE:
        logger.info("Running in MOCK mode")

        word_count=len(text.split())

        first_sentence=text.split(".")[0].strip()

        return {
            "summary": (
                f"[MOCK] Document contains {word_count} words. "
                f"[MOCK] First sentence: {first_sentence}."
            ),

            "key_points": [
                "[MOCK] Key point extraction is not available in mock mode."
            ],

            "action_items": [
                "[MOCK] Action item extraction is not available in mock mode."
            ],

            "Mode": "Mock"
        }    
    prompt=  f"""
    Summarize the following document.

    Return ONLY valid JSON with exactly these keys:

    {{
        "summary": "...",
        "key_points": ["..."],
        "action_items": ["..."]
    }}

    Do not return markdown.
    Do not return ```json.
    Do not add any text outside the JSON.

    Document:
    {text}
    """

    result= await Runner.run(agent,prompt)
    data= json.loads(result.final_output)

    if "summary" not in data:
        raise ValueError("Gemini response missing 'summary'")

    if "key_points" not in data:
        raise ValueError("Gemini response missing 'key_points'")

    if "action_items" not in data:
        raise ValueError("Gemini response missing 'action_items'")

    return data

   