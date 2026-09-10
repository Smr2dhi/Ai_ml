import json
import os
import math

from pathlib import Path
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from Assign13.looger import logger

set_tracing_disabled(True)

base_dir = Path(__file__).resolve().parent
env_file = base_dir / ".env"

load_dotenv(env_file)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")      
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

logger.info("GeMINI_API_KEY exists: %s", bool(GEMINI_API_KEY))
logger.info("GEMINI_ENDPOINT exists: %s", bool(GEMINI_ENDPOINT)) 
logger.info("GEMINI_MODEL exists: %s", bool(GEMINI_MODEL))   

def is_configured():
    return all([GEMINI_API_KEY, GEMINI_ENDPOINT, GEMINI_MODEL])

logger.info("is_configured: %s", is_configured())

MOCK_MODE = not is_configured()

def get_mode():
    return "mock" if MOCK_MODE else "gemini"

logger.info("Running in %s mode", get_mode())

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
logger.info("Embedding model loaded: %s", embedding_model)

if not MOCK_MODE:
    logger.info("Creating AsyncOpenAI client...")

    client=AsyncOpenAI(
        api_key=GEMINI_API_KEY, 
        base_url=GEMINI_ENDPOINT
    )   

    logger.info("AsyncOpenAI client created")
    model=OpenAIChatCompletionsModel(
        model=GEMINI_MODEL,     
        openai_client=client)

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
        """,

        model=model
    )
    logger.info("Agent object created")

def get_document_embedding(text):
    return embedding_model.encode_document(text).tolist()


def get_query_embedding(text):
    return embedding_model.encode_query(text).tolist()

def cosine_similarity(vec1, vec2):
    dot_product=sum(a*b for a, b in zip(vec1, vec2))
    norm1=math.sqrt(sum(a*a for a in vec1))
    norm2=math.sqrt(sum(b*b for b in vec2))
    if norm1==0 or norm2==0:
        return 0.0
    return dot_product/(norm1*norm2)

async def summarize_document(document_text):
    if MOCK_MODE:
        logger.info("[MOCK_MODE] is running ")

        word_count=len(document_text.split())
        first_sentence=document_text.split(".")[0].strip()

        return{
            "summary":(
                f"[MOCK] This is a mock summary of the document. It has {word_count} words."
                f"[MOCK] The first sentence is: {first_sentence}"
            ),
            "key_points": [
                "[MOCK] Key point extraction is not available in mock mode."
            ],

            "action_items": [
                "[MOCK] Action item extraction is not available in mock mode."
            ],

            "Mode": "Mock"
        
        }
    prompt = f"""
    Summarize this document:

    {text}
    """

    result=await Runner.run(agent, prompt)
    data=json.loads(result.final_output)

    if "summary" not in data:
        raise ValueError("Gemini response missing 'summary'")

    if "key_points" not in data:
        raise ValueError("Gemini response missing 'key_points'")

    if "action_items" not in data:
        raise ValueError("Gemini response missing 'action_items'")

    return data

