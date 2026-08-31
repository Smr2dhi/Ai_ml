import os
import logging
CONTEXT_LIMIT=3000

PROMPTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "prompts"
)


log_file=os.path.join(os.path.dirname(__file__),"prompt.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(levelname)s :%(message)s"
)
logger=logging.getLogger(__name__)

def call_llm(prompt):
    """FAKE LLM for practice. Returns canned responses - no API, no key, no network. 
    In a later session this body becomes a real LLM API call; nothing else changes.""" 
    prompt_lower = prompt.lower() 
    
    if "summarize" in prompt_lower: 
        return "SUMMARY: The document describes company policy in three key points." 
    
    if "json" in prompt_lower: 
        return '{"answer": "This is a canned JSON response from the fake LLM."}' 
   
    if "do not have enough information" in prompt_lower or "provided" in prompt_lower: 
        return "Based on the provided documents: employees receive 18 days of annual leave." 
   
    return "This is a canned response from the fake LLM stub." 

def estimate_tokens(text):
    logger.info("Token estimated")
    return round(len(text.split())*1.3)

def load_templates(name):
    path=os.path.join(PROMPTS_DIR,name+".txt")
    
    if not os.path.exists(path):
        logger.error("Template not found: %s",name)
        
        raise FileNotFoundError("No such file exists")
    
    logger.info("Loading template: %s", name)
    with open(path,"r")as file:
        return file.read()
    
def find_placeholders(template):
    placeholders=[]
    
    start=0
    
    while True:
        start_barce=template.find("{",start)
        
        if start_barce==-1:
            break
        
        end_brace=template.find("}",start_barce)
        
        if end_brace==-1:
            break
        
        name=template[start_barce+1:end_brace]
        
        if name not in placeholders:
            placeholders.append(name)
            
        start=end_brace+1
    return placeholders

    
def fill_template(template,values):
    placeholders=find_placeholders(template)
    
    for placeholder in placeholders:
        if placeholder not in values:
            
            logger.error("Misisng value")
            raise ValueError(
                "Misisng values for"+placeholder
            
        )   
    for key in values:
        if key not in placeholders:
            
            logger.error("Key not found")
            raise ValueError(
                "Extra value: " + key
            )

    filled_template = template
    for placeholder in placeholders:

        filled_template = filled_template.replace(
            "{" + placeholder + "}",
            str(values[placeholder])
            )
        
    return filled_template


def format_documents(documents):

    document_text = ""

    for document in documents:
        document_text = document_text + "Document: " + document["name"] + "\n"
        document_text = document_text + document["content"] + "\n\n"

    logger.info("Document formateed")
    return document_text


def build_answer_prompt(question,documents):
    system_text=load_templates("system")
    
    answer_template=load_templates("answer_question")
    
    document_text=format_documents(documents)
    
    values={
        "question":question,
        "documents":document_text
    }
    
    filled_template=fill_template(answer_template,values)

    full_prompt = system_text + "\n\n" + filled_template

    tokens = estimate_tokens(full_prompt)

    if tokens > CONTEXT_LIMIT:
        logger.warning(" Prompt exceeds context limit.")

    return full_prompt


def answer_question(question, documents):

    prompt = build_answer_prompt(question, documents)
    tokens = estimate_tokens(prompt)
    response = call_llm(prompt)

    result = {
        "question": question,
        "prompt_tokens_approx": tokens,
        "answer": response
    }
    logger.info("Question answered successfully")
    return result

if __name__ == "__main__":

    try:
        documents = [

            {
                "name": "HR Leave Policy",

                "content": (
                    "Employees receive 18 days of annual leave per year. "
                    "Leave must be applied 3 days in advance through the HR portal. "
                    "A maximum of 5 days can be carried forward to the next year. "
                    "Sick leave requires a medical certificate after 2 consecutive days."
                )
            },

            {
                "name": "Travel Reimbursement Policy",

                "content": (
                    "Employees may claim travel expenses within 30 days of the trip. "
                    "Claims require original receipts and manager approval. "
                    "Air travel must be booked in economy class unless approved by a director."
                )
            }
        ]



        question_1 = (
            "How many days of annual leave do employees get?"
        )

        prompt_1 = build_answer_prompt(
            question_1,
            documents
        )

        tokens_1 = estimate_tokens(prompt_1)

        print(
            "\n--- Built prompt "
            "(approx",
            tokens_1,
            "tokens) ---"
        )

        print(prompt_1)

        result_1 = answer_question(
            question_1,
            documents )

        print("\n--- Result 1 ---")
        print(result_1)


        question_2 = "What is the office wifi password?"

        result_2 = answer_question(
            question_2,
            documents )

        print("\n--- Result 2 ---")
        print(result_2)
        
    except Exception as error:
        
        logger.exception("unexpected error occured ")