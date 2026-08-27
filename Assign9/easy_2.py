def estimate_tokens(text):
    
    no_of_words=len(text.split())
    
    tokens=round(no_of_words*1.3)
    return tokens

def fits_in_context(text,context_limit):
    
    tokens =estimate_tokens(text)
    
    if tokens <= context_limit:
        return True
    
    return False

def main():
    texts=input("enter the text: ")
    length_of_text=len(texts.split())
    context_limit=40
    
    tokens=estimate_tokens(texts)
    
    result=fits_in_context(texts,context_limit)
    
    if result:
        print(f"{texts}: {length_of_text} words, approx {tokens}tokens -> FITS")
    
    else:
        print(f"{texts}: {length_of_text} words, approx {tokens}tokens -> TOO LARGE for context window")

        
    
if __name__ == "__main__":
    main()