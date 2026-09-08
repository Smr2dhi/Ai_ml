"""synonym_table.get(word, word)
                     ↑     ↑
                     │     └── if not found, keep original word
                     └──────── key to search
"""

documents = [ 
    {"title": "Automobile Coverage Guide", 
     "content": "Automobile insurance protects your vehicle."}, 
    {"title": "Vehicle Collision Protection", 
     "content": "Our plan covers repair costs after an accident."}, 
    {"title": "Employee Leave Policy", 
     "content": "Employees receive twenty days of paid leave per year."}, 
] 


synonym_table={
    "car":"vehicle",
    "automobile":"vechile",
    "collision":"vehicle",
    "insurance":"coverage",
    "protection":"coverage",
    "protects":"coverage"
}

def words_of(text,use_synonyms=False):
    words=set()

    for word in text.lower().split():
        word=word.strip(".,!?;:()\"")

        if use_synonyms:
            word=synonym_table.get(word,word)


        if len(word)>=3:
            words.add(word)

    return words


def keyword_search(query,use_synonyms=False):
    query_words=words_of(query,use_synonyms)

    results=[]

    for doc in documents:
        text=doc["title"] +" "+ doc["content"]
        doc_word=words_of(text,use_synonyms)

        matched_words=query_words & doc_word

        if matched_words:
            results.append({
                "title":doc["title"],
                "matched_words":sorted(matched_words)
            })

    return results




query = "How does car insurance  work?"


print("Query: ",query)
print("\n--- Naive keyword search ---")

for result in keyword_search(query):
    print(
        f"MATCH: {result['title']}  -->"
        f"matched words: {result['matched_words']}"
    )

print("\n--- Keyword search with a synonym table ---")

for result in keyword_search(query,use_synonyms=True):
    print(
            f"MATCH: {result['title']}  -->"
            f"matched words: {result['matched_words']}"
        )

print("conclusion:the synonym table helped, but somebody must maintain it for every word in every language. Embeddings learn meaning automatically - that is what semantic search uses. ")


""""
conclusion:A synonym table can improve keyword search,
 but someone has to manually create and maintain the 
 relationships. Embeddings are used for semantic search
   because they represent meaning, so related words can
     be found without manually listing every synonym.
"""