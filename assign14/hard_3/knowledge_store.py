from assign14.rag_helpers import chunk_text, embed_text, VectorIndex
from assign14.looger import logger

class KnowledgeStore:

    def __init__(self, chunk_size=15, overlap=3):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.records = []
        self.documents = {}

    def add_document(self, name, text):
        chunks = chunk_text(text,self.chunk_size,self.overlap)

        if not chunks:
            return 0

        if not self.records:
            vector = embed_text(chunks[0])
            self.index = VectorIndex(len(vector))

        for number, chunk in enumerate(chunks, start=1):
            vector = embed_text(chunk)
            self.index.add(vector)

            self.records.append({
                "document": name,
                "chunk_index": number,
                "text": chunk
            })

        self.documents[name] = len(chunks)

        return len(chunks)

    def search(self, question, k=3):
        if not self.records:
            return []

        query_vector = embed_text(question)
        distances, positions = self.index.search(query_vector, k)

        results = []

        for distance, position in zip(distances, positions):
            result = self.records[position].copy()
            result["distance"] = float(distance)
            results.append(result)

        return results

    def document_count(self):
        return len(self.documents)

    def chunk_count(self):
        return len(self.records)

    def document_list(self):
        result = []

        for name, chunks in self.documents.items():
            result.append({
                "name": name,
                "chunks": chunks
            })

        return result