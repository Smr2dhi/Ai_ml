import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


knowledge_base = { 
    "Leave Policy": "Employees receive 20 days of paid annual leave. Unused leave can be carried forward up to 10 days with manager approval.", 
    "Travel Policy": "Travel reimbursement claims must be submitted within 30 days with original receipts attached.", 
    "Remote Work Policy": "Employees may work remotely up to three days per week with manager approval.", 
    "IT Security Policy": "Company laptop devices must have disk encryption enabled. A lost laptop must be reported to the IT helpdesk immediately.", 
    "Employee Handbook": "The handbook covers dress code, office hours, code of conduct, and general workplace expectations.", 
} 

tests = [ 
    ("Can leave be carried forward?", "Leave Policy"), 
    ("How do I submit travel reimbursement claims?", "Travel Policy"), 
    ("Can I work remotely two days per week?", "Remote Work Policy"), 
    ("What should I do if my laptop is lost?", "IT Security Policy"), 
    ("Do I need manager approval?", "Leave Policy"), 
] 

REFUSAL_DISTANCE=float(os.getenv("REFUSAL_DISTANCE", "1.7"))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

records = [
    {"document": name, "chunk_index": 1, "text": text}
    for name, text in knowledge_base.items()
]

index = VectorIndex(len(embed_text(records[0]["text"])))

for record in records:
    index.add(embed_text(record["text"]))

def retrieve(question, k):
    distances, positions = index.search(embed_text(question), k)

    return [
        dict(records[pos], distance=round(dist, 3))
        for dist, pos in zip(distances, positions)
    ]


def evaluate(k):
    hits=0

    for question, expected in tests:
        names = [c["document"] for c in retrieve(question, k)]

        if expected in names:
            hits += 1

    return hits



print("=== Retrieval Quality Report ===")

for question, expected in tests:
    results = retrieve(question, 3)

    top1 = results[0]

    if top1["document"] == expected:
        print("HIT@1")
    else:
        print("MISS@1")

    found = False

    for result in results:
        if result["document"] == expected:
            found = True
            break

    if found:
        print("HIT@3")
    else:
        print("MISS@3")

    print("Question:", question)
    print("Expected:", expected)
    print("Top-1:", top1["document"])
    print()


hits1 = evaluate(1)
hits3 = evaluate(3)

print("Hit rate @1:", hits1, "/", len(tests))
print("Hit rate @3:", hits3, "/", len(tests))


print("=== Ambiguous Question ===")

question = "Do I need manager approval?"
results = retrieve(question, 3)

for result in results:
    print(result["document"], result["distance"])


async def answer(question):
    result = retrieve(question, 1)[0]

    print()
    print("Question:", question)
    print("Best document:", result["document"])
    print("Distance:", result["distance"])

    if result["distance"] > REFUSAL_DISTANCE:
        print("Answer: I do not know based on the current knowledge base.")
        return

    results = retrieve(question, 3)
    prompt = build_prompt(question, results)
    answer = await generate_answer(prompt, results)

    print("Answer:", answer)


import asyncio

asyncio.run(answer("Can leave be carried forward?"))
asyncio.run(answer("What is the cafeteria menu today?"))