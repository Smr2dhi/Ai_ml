from assign14 import ai_client
import hashlib
from assign14.logger import logger
import math
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

documents = [ 
    "Automobile insurance protects your vehicle.", 
    "Home loans require income proof.", 
    "The cafeteria menu changes weekly.", 
    "remote work document allowed"
]

question = "is whf allowed" 

for doc in documents:
    if "car" in doc.lower():
        print(doc)
print("Not Found")


synonyms={
    "car": "automobile",
     "vehicle": "automobile",
     "wfh":"remote"
}


            
async def mock_embed(text):
    words=text.lower().split()
    vector=[0.0]*10

    for word in words:
        word=synonyms.get(word,word)

        index=int(hashlib.md5(word.encode()).hexdigest(),16)%10

        vector[index]+=1

    length=math.sqrt(sum(x*x for x in vector))

    if length == 0:
        return vector

    return [x/length for x in vector] #normalize the vector


async def main():
    try:
        question_vector= ai_client.get_query_embedding(question)
        logger.info("Ai mode")

        best_score=-1.0
        best_doc=None

        for doc in documents:
            doc_vector=  ai_client.get_document_embedding(doc)

            similarity_score=ai_client.cosine_similarity(question_vector,doc_vector)
            print(f"Similarity_score between question and document: {similarity_score}")

            print(round(similarity_score,4))

            if similarity_score>best_score:
                best_score=similarity_score
                best_doc=doc
        print(f"Best document: {best_doc} with similarity score: {round(best_score,4)}")
    
    except Exception as e:
        logger.warning(f"Ai embedding failed: {e}")

        print("Mock response")

        question_vector=await mock_embed(question)
        best_score=-1.0
        best_doc=None

        for doc in documents:
            doc_vector=await mock_embed(doc)

            similarity_score=ai_client.cosine_similarity(question_vector,doc_vector)
            print(f"Similarity_score between question and document: {similarity_score}")

            print(round(similarity_score,4))

            if similarity_score>best_score:
                best_score=similarity_score
                best_doc=doc

        print(f"Best document: {best_doc} with similarity score: {round(best_score,4)}")

if __name__=="__main__":
    import asyncio
    asyncio.run(main())



    



