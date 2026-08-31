CONTEXT_LIMIT=500

library= [
    {
        "name": "summarize_document", "use_case": "Summarize a policy document", 
"template": "...full prompt with {document}...", "placeholders": ["document"]
} 
{
    "name": "extract_contact", "use_case": "Extract contact info as JSON", 
"template": "...full prompt with {text}...", "placeholders": ["text"]
} 
{
    "name": "support_answer", "use_case": "Answer from policy only", 
"template": "...full prompt with {question} and {policy}...", "placeholders": ["question", "policy"]
} 
]

def estimate_tokens(text):
    word=len(text.split())
    tokens=round(word*1.3)
    return tokens

def find_placeholders(template):
    placeholders=[]

    start=0

    while True:
        start_barces=template.find("{",start)
        if start_barces ==-1:
            break

        end_brace=template.find("}",start_barces)
        if end_brace ==-1:
            break

        placeholder=template[start_barces+1:end_brace]

        if placeholder not in placeholders:
            placeholders.append(placeholder)

        start_barces=end_brace+1
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
        print(data["name","-",data["use_case"]])


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