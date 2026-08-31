import json
import logging
import os

log_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),"app.log")


logging.basicConfig(
    filename="validation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

FAKE_RESPONSES = [
    'Sure! Here is the extracted data: {"employee": "Priya", "department": "Finance"}',
    '{"employee": "Priya", "department": "Finance"}',
    '{"employee": "Priya", "department": "Finance", "issue_type": "reimbursement"}'
]
call_count=0

def call_llm(prompt):
    """Fake LLM that misbehaves on early attempts."""

    global call_count
    response = FAKE_RESPONSES[
        min(call_count, len(FAKE_RESPONSES) - 1)]

    call_count += 1
    return response

def validate_response(text,required_keys):

    try:
        data=json.loads(text)
        
    except json.JSONDecodeError as e:
        return False,f"Invalid json: {e}"
    
    missing_keys=[]
    for key in required_keys:
        if key not in data:
            missing_keys.append(key)
            
    if missing_keys:
        return False , f"missing keys: {missing_keys}"
    
    return True,data

def extract_with_retry(base_prompt,required_keys,max_attempts=3):
    prompt=base_prompt
    
    for attempt in range(1,max_attempts+1):
        response= call_llm(prompt)
        
        is_valid,validate_data=validate_response(response,required_keys)
        
        if is_valid:
            print(f"Attempt {attempt}: Success")
            logging.info(f"Attempt {attempt}: Success")
            return validate_data
        
        print(f"Attempted {attempt}:Failed -{validate_data}")
    
        prompt = ( base_prompt + f"\nYour previous response was rejected: {validate_data}."
            + f"\nReturn JSON only with keys: {required_keys}."
            + "\nNo other text."
        )

    raise ValueError(f"LLM output failed validation after {max_attempts} attempts")
    

def main():
    global call_count
    
    required_keys=["employee","department","issue_type"]
    
    base_prompt="""Extract employee, department, and issue_type.
                    Return JSON only."""
    
    print("First test")
    result=extract_with_retry(base_prompt,required_keys)
    
    print("Validated results:",result)
    
    print()
    print("___With max_attempst+2--")
    
    call_count=0

    try:
        extract_with_retry( base_prompt, required_keys, max_attempts=2)

    except ValueError as e:
        print(e)




if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        logger.exception("Unexpected error")
        print("Unexpected error:", e)