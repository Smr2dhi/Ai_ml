import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from assign14.hard_3.knowledge_store import KnowledgeStore
from assign14.rag_helpers import (
    generate_answer,
    build_context,
    get_mode
)
from assign14.looger import logger


app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.3"
)


SEED_DOCUMENTS = {
    "Leave Policy": (
        "Employees receive twenty days of paid annual leave every calendar year. "
        "Unused leave can be carried forward up to ten days with manager approval. "
        "Carry forward requests must be submitted in December through the HR portal."
    ),

    "Travel Policy": (
        "Travel reimbursement claims must be submitted within thirty days of the trip. "
        "Original receipts are required for flights hotels and taxis. "
        "International travel requires prior approval from the department head."
    ),

    "Remote Work Policy": (
        "Employees may work remotely up to three days per week. "
        "Remote work requires manager approval and a stable internet connection."
    ),
}


REFUSAL_DISTANCE = float(
    os.getenv("REFUSAL_DISTANCE", "1.4")
)


class DocumentRequest(BaseModel):
    name: str = Field(min_length=1)
    text: str = Field(min_length=1)


class DocumentResponse(BaseModel):
    document: str
    chunks_stored: int
    total_chunks: int


class DocumentInfo(BaseModel):
    name: str
    chunks: int


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class SourceCitation(BaseModel):
    document: str
    chunk_index: int
    snippet: str
    distance: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceCitation]
    mode: str


class RootResponse(BaseModel):
    app: str
    version: str
    mode: str
    documents: int
    chunks: int


class RagPipeline:

    def __init__(self, store):
        self.store = store

    def retrieve(self, question, top_k):
        return self.store.search(question, top_k)

    def filter(self, chunks):
        return [chunk for chunk in chunks
            if chunk["distance"] <= REFUSAL_DISTANCE
        ]

    def build_prompt(self, question, chunks):
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

    async def generate(self, prompt, chunks):
        return await generate_answer(prompt, chunks)

    def cite(self, chunks):
        sources = []

        for chunk in chunks:
            words = chunk["text"].split()
            snippet = " ".join(words[:12])

            if len(words) > 12:
                snippet += "..."

            sources.append(
                SourceCitation(
                    document=chunk["document"],
                    chunk_index=chunk["chunk_index"],
                    snippet=snippet,
                    distance=round(chunk["distance"], 3)
                )
            )

        return sources

    async def answer(self, question, top_k):
        chunks = self.retrieve(question, top_k)

        chunks = self.filter(chunks)
        if not chunks:
            return AskResponse(
                question=question,
                answer="I do not know based on the current knowledge base.",
                sources=[],
                mode=get_mode()
            )

        prompt = self.build_prompt(question, chunks)
        answer = await self.generate(prompt,chunks)
        sources = self.cite(chunks)

        return AskResponse(
            question=question,
            answer=answer,
            sources=sources,
            mode=get_mode()
        )


store = KnowledgeStore(chunk_size=15,overlap=3)

pipeline = RagPipeline(store)

@app.on_event("startup")
async def startup():
    for name, text in SEED_DOCUMENTS.items():
        store.add_document(name, text)


@app.get("/", response_model=RootResponse)
def root():
    return RootResponse(
        app="AI Knowledge Assistant",
        version="1.3",
        mode=get_mode(),
        documents=store.document_count(),
        chunks=store.chunk_count()
    )


@app.get(
    "/documents",
    response_model=list[DocumentInfo]
)
def documents():
    return store.document_list()


@app.post(
    "/documents",
    response_model=DocumentResponse
)
def add_document(request: DocumentRequest):

    if request.name in store.documents:
        raise HTTPException(
            status_code=409,
            detail="Document already exists"
        )

    chunks = store.add_document(
        request.name,
        request.text
    )

    return DocumentResponse(
        document=request.name,
        chunks_stored=chunks,
        total_chunks=store.chunk_count()
    )


@app.post(
    "/ask",
    response_model=AskResponse
)
async def ask(request: AskRequest):

    return await pipeline.answer(
        request.question,
        request.top_k
    )