import faiss
import numpy as np

from assign14 import ai_client

def chunk_text(text,chunk_size,overlap):

	words = text.split()
	chunks=[]

	start=0
	while start<len(words):
		chunks.append(" ".join(words[start:start+chunk_size]))
		start+=chunk_size-overlap
	return chunks



class KnowledgeStore:
	def __init__(self,chunk_size=15,overlap=3):
		self.index=None
		self.records=[]


	def add_document(self,name,text):
		chunks=chunk_text(text,chunk_size=15,overlap=3)

		for chunk_index,chunk in enumerate(chunks,start=1):
			vector=ai_client.get_document_embedding(chunk)
			vector =np.array([vector],dtype="float32")

			if self.index is None:
				self.index =faiss.IndexFlatL2(len(vector[0]))

			self.index.add(vector)

			self.records.append({
				"document":name,
				"chunk_index":chunk_index,
				"text":chunk
			})
	def search(self,question,k=3):
		if self.index is None:
			return []
			

		vector=ai_client.get_document_embedding(question)
		vector=np.array([vector],dtype="float32")

		distances,indexes=self.index.search(vector,k)

		results=[]

		for distance,index in zip(distances[0],indexes[0]):
			result=self.records[index].copy()
			result["distance"]=float(distance)
			results.append(result)

		return results

	def stats(self):
		documents = set()
		for record in self.records:
			documents.add(record["document"])

		return {
			"document_count": len(documents),
			"chunk_count": len(self.records)
		}
 
leave_text = ("Employees receive twenty days of paid annual leave every calendar year. " 
              "Unused leave can be carried forward up to ten days with manager approval. " 
              "Carry forward requests must be submitted in December through the HR portal.") 
travel_text = ("Travel reimbursement claims must be submitted within thirty days of the trip. " 
               "Original receipts are required for flights hotels and taxis. " 
               "International travel requires prior approval from the department head.") 
 

store= KnowledgeStore()

store.add_document("Leave Policy",leave_text)
store.add_document("Travel Policy",travel_text)

stats=store.stats()
print("knowledgeStore:",stats["documents"])
print("documents: ",stats["chunks"])

question = "Can unused leave be carried forward?" 

print("Question:", question)

for rank, result in enumerate(store.search(question, k=2), start=1): 
    print(
        f"{rank}. {result['document']} "
        f"(chunk {result['chunk_index']}) "
        f"distance {result['distance']}"
    )
    print(f"   {result['text']}")