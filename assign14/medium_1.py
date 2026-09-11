import numpy as np
from sentence_transformers import SentenceTransformer

try:
	import faiss
	faiss_available = True
except ImportError:
	faiss_available =False

knowledge = [ 
    {"text": "The employee handbook covers office hours, dress code, and workplace conduct.", 
     "metadata": {"document_name": "Employee Handbook", "category": "HR", "source": "PDF"}}, 
    {"text": "Employees receive 20 days of annual leave. Unused leave can be carried forward up to 10 days.", 
     "metadata": {"document_name": "Leave Policy", "category": "HR", "source": "PDF"}}, 
    {"text": "Travel reimbursement claims must be submitted within 30 days with receipts.", 
     "metadata": {"document_name": "Travel Policy", "category": "Finance", "source": "DOCX"}}, 
    {"text": "Laptops must use disk encryption and lost devices must be reported to the IT helpdesk.", 
     "metadata": {"document_name": "IT Policy", "category": "IT", "source": "Wiki"}}, 
] 

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts=[item["text"] for item in knowledge]
embeddings=model.encode_document(texts)

vectors=np.array(embeddings,dtype="float32")

if faiss_available:
	dimension=vectors.shape[1]
	index=faiss.IndexFlatL2(dimension)

	index.add(vectors)

else:
	index=vectors

search_count=0

def main():
	while True:
		question=input("Enter your query or 'q' for quit: ")
		if question.lower()=='q':
			break

		search_count+=1
		query_embedding=model.encode_query([question])
		query_vector=np.array(query_embedding,dtype="float32")

		distances,positions =index.search(query_vector,3)

		print("\ntop 3 results:")

		for rank ,(position,distance) in enumerate(
			zip(positions[0],distances[0]),start=1
		):
			result=knowledge[position]
			metadata=result["metadata"]

			print(f"\nRank: {rank}")
			print(f"Document: {metadata['document_name']}")
			print(f"Category: {metadata['category']}")
			print(f"Source: {metadata['source']}")
			print(f"Distance: {distance:.4f}")
			print(f"Text: {result['text']}")

	print(f"\nTotal searches performed: {search_count}")
	
		

if __name__ =="__main__":
	main()