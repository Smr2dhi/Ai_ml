from pydantic import BaseModel,ValidationError
from typing import List

class ResumeProfile(BaseModel): 
    name: str 
    skills: List[str] 
    experience_years: int 

mock_responses = [ 
    'Sure! Here is the profile:\n{"name": "Arjun Mehta", "skills": ["Python", "FastAPI", "SQL"], "experience_years": 5}', 
    '{"name": "Beena Thomas", "skills": "Java, Spring, Kafka", "experience_years": "8"}', 
    '{"name": "Chirag Rao", "skills": ["JavaScript", "React"]}', 
]

def extract_json_black(text:str)->str:
    start=text.find("{")
    end=text.rfind("}")

	
    if start == -1 and end == -1:
        return text
    return text[start :end+1]


def build_prompt(resume_text:str)->str:
    return f"""
task : extract information from the resume
return only valid JSON object

use this exact schema:
{{
    "name": "string",
    "skills": ["string"],
    "experience_years": "number"
}}

Allowed types:
- name: string
- skills: list of strings
- experience_years: integer

{resume_text}
"""

