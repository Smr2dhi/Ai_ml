from Assign12.llmClient import ask_llm
from Assign12.utils import logger
import json
from pydantic import ValidationError


def extract_json_block(text):
    start=text.find("{")
    end=text.rfind("}")

    if start == -1 or end == -1:
        return text
    return text[start:end+1]

def ask_for_model(prompt,model_cls,mock_response,max_attempts=3):
    for attempt in range(max_attempts):
        try:
            response=ask_llm(prompt,mock_response)
            json_text = extract_json_block(response)

            data=json.loads(json_text)
            result=model_cls(**data)

            logger.info(f"Attempt {attempt + 1}: successful")
            return result

        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Attempt {attempt + 1}: failed - {e}")

            prompt = prompt + "\nReturn ONLY valid JSON."

    raise ValueError("Model extraction failed after all attempts")