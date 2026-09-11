import asyncio
from assign14.ai_client import (
    MOCK_MODE,
    chunk_text,
    embed_text,
    VectorIndex,
    generate_answer,
    RAG_ANSWER_TEMPLATE
)
DOCUMENTS = { 
    "Leave Policy": ("Employees receive twenty days of paid annual leave every year. " 
                     "Unused leave can be carried forward up to ten days with manager approval."), 
    "Travel Policy": ("Travel reimbursement claims must be submitted within thirty days " 
                      "with original receipts."), 
    "Remote Work Policy": ("Employees may work remotely up to three days per week " 
                           "with manager approval."), 
    "IT Security Policy": ("Company laptop devices must use disk encryption. " 
                           "A lost laptop must be reported to the IT helpdesk immediately."), 
    "Employee Handbook": ("The handbook covers dress code, office hours, code of conduct, " 
                          "and workplace expectations."), 
    "Health Benefits Guide": ("Medical insurance covers employees and dependents. " 
                              "Claims are processed within fifteen working days."), 
    "Expense Policy": ("Business expenses require pre-approval above one hundred dollars " 
                       "and itemized receipts."), 
    "Onboarding Guide": ("New hires complete orientation, security training, and system " 
                         "access setup in the first week."), 
    "Payroll FAQ": ("Salaries are paid on the last working day of each month. " 
                    "Payslips are available on the portal."), 
    "Training Catalog": ("Employees may enroll in technical and leadership training " 
                         "programs each quarter."), 
} 

records = []
vectors = []

for name, text in DOCUMENTS.items():
    chunks = chunk_text(
        text,
        chunk_size=25,
        overlap=5)

    for number, chunk in enumerate(chunks, start=1):
        vector = embed_text(chunk)
        vectors.append(vector)

        records.append({
            "document": name,
            "chunk_index": number,
            "text": chunk})

index = VectorIndex(len(vectors[0]))
for vector in vectors:
    index.add(vector)


def retrieve(question, k=3):
    query_vector = embed_text(question)

    distances, positions = index.search(query_vector,k)
    chunks = []

    for distance, position in zip(distances, positions):
        chunk = records[position].copy()
        chunk["distance"] = distance
        chunks.append(chunk)

    return chunks
    
def build_prompt(question, chunks):
    context = "\n".join(
        f"[{chunk['document']} - chunk {chunk['chunk_index']}] "
        f"{chunk['text']}"
        for chunk in chunks)

    return RAG_ANSWER_TEMPLATE.format(
        context=context,
        question=question)

async def main():
    question_count = 0

    while True:
        question = input("\nQuestion: ").strip()

        if not question:
            continue

        if question.lower() == "q":
            break

        question_count += 1

        chunks = retrieve(question, k=3)

        print("\nRetrieved Context:")

        for rank, chunk in enumerate(chunks, start=1):
            print(
                f"{rank}. [{chunk['document']} - "
                f"chunk {chunk['chunk_index']}] "
                f"distance={chunk['distance']:.3f}"
            )
            print(f"   {chunk['text']}")

        prompt = build_prompt(question, chunks)

        answer = await generate_answer(
            prompt,
            chunks
        )

        print("\nAnswer:")
        print(answer)

        print("\nSources:")

        sources = []

        for chunk in chunks:
            if chunk["document"] not in sources:
                sources.append(chunk["document"])

        for source in sources:
            print(f"- {source}")

    print(f"\nQuestions asked: {question_count}")


if __name__ == "__main__":
    asyncio.run(main())