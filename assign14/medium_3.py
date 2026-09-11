from assign14 .rag_helpers import (
	embed_text,
	VectorIndex,
	build_context,
	generate_answer)
import asyncio


RAG_ANSWER_TEMPLATE = """You are the AI Knowledge Assistant for our company.
Use ONLY the context below to answer the question.
If the answer is not in the context, reply exactly:
I do not know based on the current knowledge base.

Context:
{context}

Question:
{question}

Answer:
"""


documents = { 
    "Leave Policy": "Unused leave can be carried forward up to ten days with manager approval.", 
    "Travel Policy": "Travel reimbursement claims must be submitted within thirty days.", 
    "Remote Work Policy": "Employees may work remotely three days per week with manager approval.", 
} 


def retrieve(question, k=2):

	records = []
	index = None

	for name,text in documents.items():
		vector=embed_text(text)

		if index is None:
			index=VectorIndex(len(vector))

		index.add(vector)

		records.append({
			"document": name,
			"chunk_index": 1,
			"text": text

		})


	query_vector = embed_text(question)

	distances, positions = index.search(query_vector, 2)
	chunks = []

	for distance, position in zip(distances, positions):
		chunk = records[position].copy()
		chunk["distance"] = distance
		chunks.append(chunk)
	return chunks

def build_prompt(question,chunks):
	context=build_context(chunks)

	return RAG_ANSWER_TEMPLATE.format(
		context=context,
		question=question
	)
async def main():
    question = "Can unused leave be carried forward without manager approval?"

    chunks = retrieve(question, k=2)
    prompt = build_prompt(question, chunks)

    print("FULL ASSEMBLED PROMPT:")
    print(prompt)
    answer = await generate_answer(prompt, chunks)

    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())