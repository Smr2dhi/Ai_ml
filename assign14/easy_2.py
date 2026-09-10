from assign14.easy_1 import mock_embed
import faiss
import numpy as np
import asyncio

documents = [ 
    "Leave policy: unused leave can be carried forward with approval.", 
    "Travel policy: travel reimbursement claims need receipts.", 
    "Remote work policy: employees may work remotely three days per week.", 
    "IT policy: laptops must use disk encryption.", 
] 

async def main():
		
	embeddings=[await mock_embed(doc) for doc in documents]

	dimension=len(embeddings[0])

	index=faiss.IndexFlatL2(dimension)

	vectors=np.array(embeddings,dtype="float32")
	# np.array() = convert my list into a numerical array that libraries like FAISS can work with.
	index.add(vectors) #Store these document vectors inside the FAISS index."

	question="How do travel claims work?"

	question_vector= await mock_embed(question)

	query =np.array([question_vector],dtype="float32")
	# Why [question_vector]?
	# Because FAISS expects the query in a 2D array format:

	distances,positions=index.search(query,1)
	# distances->FAISS calculates how far the question vector is from each document vector.
	#smaller num closer vector are

	#position/indices->means the positions/indices of the matching documents.

	print("Top 1: ")
	position=positions[0][0]
	distance=distances[0][0]

	print(f"Document {documents[position]}")
	print(f"Distance: {distance}")

	d,p=index.search(query,4)

	print("full ranking...")
	for dist,pos in zip(d[0],p[0]):
	# . Why d[0] and p[0]?
	# FAISS returns results in a 2D structure because you can search multiple queries at once.
	# You have only one question. so d[0]

		print(round(dist,3)," ",documents[pos])
if __name__ == "__main__":
	asyncio.run(main())
	# zip ->Suppose:

	# d[0] = [0.21, 1.31, 1.82, 2.04]

	# p[0] = [1,    2,    0,    3]

	# zip() pairs them:

	# (0.21, 1)
	# (1.31, 2)
	# (1.82, 0)
	# (2.04, 3)

	"""
						DOCUMENTS
							│
			┌──────────────┼──────────────┐
			↓              ↓              ↓
		Leave          Travel          Remote ...
			│              │              │
			└──────────────┼──────────────┘
							↓
						embed_text()
							↓
						EMBEDDINGS
							│
							│
					len(embeddings[0])
							│
							↓
						dimension
							│
							↓
				┌──────────────────┐
				│      FAISS       │
				│   IndexFlatL2    │
				└──────────────────┘
							↑
							│
						index.add()
							│
							│
				DOCUMENT VECTORS
							│
							│
							│
	USER QUESTION             │
	"How do travel             │
	claims work?"             │
		│                   │
		↓                   │
	embed_text()              │
		│                   │
		↓                   │
	QUESTION VECTOR            │
		│                   │
		↓                   │
		query                 │
		│                   │
		└───────→ search ───┘
						│
						↓
				d = distances
				p = positions
						│
						↓
				zip(d[0], p[0])
						│
						↓
				documents[pos]
						│
						↓
			BEST MATCHING DOCUMENT
	"""