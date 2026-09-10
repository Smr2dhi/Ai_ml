def chunk_text(text,chunk_size,overlap):

	words = text.split()
	chunks=[]

	start=0
	while start<len(words):
		chunks.append(" ".join(words[start:start+chunk_size]))
		start+=chunk_size-overlap
	return chunks

text = ("Employees receive twenty days of annual leave every year. " 
        "Unused leave can be carried forward up to ten days. " 
        "Carry forward requests need manager approval in December.") 

chunk_size=10
overlap=3

words=text.split()

print("total words: ",len(words))
print("Chunk size: ",chunk_size ,"words_overlap: ",overlap)

chunks=chunk_text(text,chunk_size,overlap)
for num,chunk in enumerate(chunks,start=1):

	print(f"[Chunk {num}]: {chunk}")

print(len(chunks),"chunks created")