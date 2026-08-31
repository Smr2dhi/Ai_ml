CONTEXT_LIMIT=500

library= [
    {
        "name": "summarize_document", "use_case": "Summarize a policy document", 
"template": "...full prompt with {document}...", "placeholders": ["document"]
} ,
{
    "name": "extract_contact", "use_case": "Extract contact info as JSON", 
"template": "...full prompt with {text}...", "placeholders": ["text"]
} ,
{
    "name": "support_answer", "use_case": "Answer from policy only", 
"template": "...full prompt with {question} and {policy}...", "placeholders": ["question", "policy"]
} 
]



def estimate_tokens(text):
    word=len(text.split())
    tokens=round(word*1.3)
    return tokens

def fits_in_context(text, context_limit):

    tokens = estimate_tokens(text)

    if tokens <= context_limit:
        return True

    return False


def find_placeholders(template):

    placeholders = []
    start = 0

    while True:
        start_brace = template.find("{", start)

        if start_brace == -1:
            break

        end_brace = template.find("}", start_brace)

        if end_brace == -1:
            break

        placeholder = template[start_brace + 1:end_brace]

        if placeholder not in placeholders:
            placeholders.append(placeholder)

        start = end_brace + 1

    return placeholders


def fill_template(template, placeholders):

    filled_template = template
    for placeholder in placeholders:

        value = input(f"Value for {{{placeholder}}}: ")
        if value == "":
            print("Value cannot be empty.")
            return None

        filled_template = filled_template.replace(
            "{" + placeholder + "}",
            value
        )

    return filled_template

def call_llm(filled_prompt):

    if "summarization" in filled_prompt.lower():
        return "SUMMARY: The document describes company policy in three key points."

    elif "contact information" in filled_prompt.lower():
        return '{"name": "", "email": "", "phone": ""}'

    elif "policy" in filled_prompt.lower():
        return "ANSWER: The answer is based only on the provided policy."

    else:
        return "FAKE LLM RESPONSE: Response generated successfully."


def list_templates():

    print("\n---Templates---")
    if len(library)==0:
        print("Library is empty.")
        return 
    
    for data in library:
        print(data["name"],"-",data["use_case"])


def view_template():
    name=input("Template name: ").strip()

    if name=="":
        print("template cannot be empty")
        return
    
    for data in library:
        if data["name"]==name:

            print("\n --Template---")
            print(data["template"])

            return

print("Template not found")


def fill_and_send():
    name=input("Template name: ").strip()

    if name=="":
        print("Tempalte name cannot be empty")
        return

    for data in library:
        if data["name"]==name:
            placeholders=find_placeholders(data["template"])
            
            filled_prompt=fill_template(data["template"],placeholders)


            if filled_prompt is None:
                return
            
            tokens=estimate_tokens(filled_prompt)
            
            print(f"Filled prompt (approx {tokens} tokens)--")
            print(filled_prompt)
            
            result=fits_in_context(filled_prompt,CONTEXT_LIMIT)
            
            if result:
                response=call_llm(filled_prompt)
                print("---LLm Response--")
                
                print(response)
                
            else:
                print("prompt excceds, conext limit")
                
            return
        print("Template not found")
        
def add_template():
    
    name=input("template namae: ").strip()
    
    if name=="":
        print("template cannot be emty")
        return
    
    for data in library:
        if data["name"]==name:
            print("Tempalte already exists.")
            return
        
    use_case=input("use case: ").strip()
    
    if use_case== "":
        print("use case cannot be empty")
        return
    
    template=input("template text: ")
    if template == "":
        print("Template cannot be empty.")
        return
    
    template=template.replace("\\n","\n")
    
    placeholders = find_placeholders(template)

    new_template = {
        "name": name,
        "use_case": use_case,
        "template": template,
        "placeholders": placeholders
    }

    library.append(new_template)
    print("Template added successfully")

def library_stats():
    print("--Library stats--")    
    
    print("Templates:", len(library))
    total_tokens=0
    
    for data in library:
        total_tokens+=estimate_tokens(data["template"])
        
    print("total approx tokens:",total_tokens)    
    
    
    max_placeholders=library[0]
    
    for data in library:
        if len(data["placeholders"])>len(max_placeholders["placeholders"]):
            max_placeholders=data
            
    print("max placeholders: ",max_placeholders["name"], len(max_placeholders["placeholders"]))
                






def show_menu():

    print()
    print("=== Prompt Library ===")

    print("""1. List Templates
2. View Template
3. Fill & Send Template
4. Add Template
5. Library Stats
6. Exit""")


def main():

    while True:

        show_menu()

        choice = input("Choice: ")

        if choice == "1":
            list_templates()

        elif choice == "2":
            view_template()

        elif choice == "3":
            fill_and_send()

        elif choice == "4":
            add_template()

        elif choice == "5":
            library_stats()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()