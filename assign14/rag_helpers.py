
import os
import hashlib
import math
from pathlib import Path

import numpy as np
import faiss

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from Assign13.looger import logger


set_tracing_disabled(True)


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


logger.info(
    "GEMINI_API_KEY exists: %s",
    bool(GEMINI_API_KEY)
)

logger.info(
    "GEMINI_ENDPOINT exists: %s",
    bool(GEMINI_ENDPOINT)
)

logger.info(
    "GEMINI_MODEL exists: %s",
    bool(GEMINI_MODEL)
)

logger.info(
    "EMBEDDING_MODEL: %s",
    EMBEDDING_MODEL
)


def is_configured():
    return all([
        GEMINI_API_KEY,
        GEMINI_ENDPOINT,
        GEMINI_MODEL
    ])


logger.info(
    "is_configured: %s",
    is_configured()
)


MOCK_MODE = not is_configured()


def get_mode():
    return "mock" if MOCK_MODE else "gemini"


if not MOCK_MODE:

    logger.info("Creating AsyncOpenAI client...")

    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url=GEMINI_ENDPOINT
    )

    logger.info("AsyncOpenAI client created")

    model = OpenAIChatCompletionsModel(
        model=GEMINI_MODEL,
        openai_client=client
    )

    logger.info("Gemini model object created")

    agent = Agent(
        name="RAG Knowledge Assistant",

        instructions="""
        You are the AI Knowledge Assistant for our company.

        Use ONLY the context provided by the user to answer the question.

        If the answer is not in the context, reply exactly:

        I do not know based on the current knowledge base.

        Do not use outside knowledge.
        """,

        model=model
    )

    logger.info("RAG agent created")


logger.info("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

logger.info("Embedding model loaded")


def mock_embed(text):

    EMBED_DIM = 256

    SYNONYMS = {
        "car": "automobile",
        "vehicle": "automobile",
        "wfh": "remote"
    }

    vector = [0.0] * EMBED_DIM

    for raw in text.lower().split():

        word = raw.strip(".,!?:;()\"'")

        word = SYNONYMS.get(
            word,
            word
        )

        if word:

            slot = int(
                hashlib.md5(
                    word.encode()
                ).hexdigest(),
                16
            ) % EMBED_DIM

            vector[slot] += 1.0

    norm = math.sqrt(
        sum(v * v for v in vector)
    ) or 1.0

    return [
        v / norm
        for v in vector
    ]


def embed_text(text):

    if MOCK_MODE:
        logger.info("Using mock embedding")

        return mock_embed(text)

    logger.info("Creating Transformer embedding")

    embedding = embedding_model.encode(
        text
    )

    return embedding.tolist()


def chunk_text(
    text,
    chunk_size=15,
    overlap=3
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        chunks.append(
            " ".join(
                words[
                    start:start + chunk_size
                ]
            )
        )

        start += chunk_size - overlap

    return chunks


try:

    import faiss
    import numpy as np

    HAS_FAISS = True

    logger.info("FAISS is available")

except ImportError:

    HAS_FAISS = False

    logger.info(
        "FAISS not available. Using in-memory fallback."
    )


class VectorIndex:

    def __init__(self, dimension):

        self.dimension = dimension

        self.count = 0

        if HAS_FAISS:

            self.index = faiss.IndexFlatL2(
                dimension
            )

        else:

            self.vectors = []


    def add(self, vector):

        if HAS_FAISS:

            self.index.add(
                np.array(
                    [vector],
                    dtype="float32"
                )
            )

        else:

            self.vectors.append(vector)

        self.count += 1


    def search(self, query, k):

        k = min(
            k,
            self.count
        )

        if k == 0:

            return [], []


        if HAS_FAISS:

            distances, positions = self.index.search(
                np.array(
                    [query],
                    dtype="float32"
                ),
                k
            )

            return (
                [
                    float(d)
                    for d in distances[0]
                ],
                [
                    int(p)
                    for p in positions[0]
                ]
            )


        scored = sorted(

            (
                sum(
                    (a - b) ** 2
                    for a, b in zip(
                        query,
                        vector
                    )
                ),
                position
            )

            for position, vector
            in enumerate(self.vectors)

        )[:k]


        return (
            [
                distance
                for distance, _
                in scored
            ],

            [
                position
                for _, position
                in scored
            ]
        )


def backend_name():

    if HAS_FAISS:

        return "FAISS IndexFlatL2"

    return "in-memory fallback"


def build_context(chunks):

    lines = []

    for chunk in chunks:

        lines.append(
            "["
            + chunk["document"]
            + " - chunk "
            + str(chunk["chunk_index"])
            + "] "
            + chunk["text"]
        )

    return "\n".join(lines)


def build_prompt(question, chunks):

    context = build_context(chunks)

    return f"""
    You are the AI Knowledge Assistant for our company.

    Use ONLY the context below to answer the question.

    If the answer is not in the context, reply exactly:

    I do not know based on the current knowledge base.

    Context:

    {context}

    Question:

    {question}

    Answer:
    """


async def generate_answer(prompt, chunks):

    if not chunks:

        return "I do not know based on the current knowledge base."


    if MOCK_MODE:

        logger.info(
            "Generating answer in MOCK mode"
        )

        best = chunks[0]

        return (
            "According to "
            + best["document"]
            + ": "
            + best["text"].strip()
        )


    logger.info(
        "Generating answer using Gemini"
    )

    result = await Runner.run(
        agent,
        prompt
    )

    return result.final_output

