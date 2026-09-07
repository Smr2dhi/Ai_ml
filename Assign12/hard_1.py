from pydantic import BaseModel,ValidationError
from Assign12.utils import logger
from typing import List
import json
import sys

class ResumeProfile(BaseModel): 
    name: str 
    skills: List[str] 
    experience_years: int 

class ScriptedLLM:
    def __init__(self,responses):
        self.responses=responses
        self.index=0

    def generate(self,prompt):
        response=self.responses[self.index]
        self.index+=1
        return response


mock_responses = [ 
    'Sure! Here is the profile:\n{"name": "Arjun Mehta", "skills": ["Python", "FastAPI", "SQL"], "experience_years": 5}', 
    '{"name": "Beena Thomas", "skills": "Java, Spring, Kafka", "experience_years": "8"}', 
    '{"name": "Chirag Rao", "skills": ["JavaScript", "React"]}', 
]


RESUMES = [ 
    "Arjun Mehta. Backend developer, 5 years. Python, FastAPI, SQL.", 
    "Beena Thomas. Senior engineer, 8 years. Java, Spring, Kafka.", 
    "Chirag Rao. Frontend developer. JavaScript, React.", 
] 


def extract_json_block(text:str)->str:
    start=text.find("{")
    end=text.rfind("}")

	
    if start == -1 or end == -1:
        return text
    return text[start :end+1]


def build_prompt(resume_text):
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

def repair_types(data):
    repairs=[]

    if isinstance(data.get("skills"),str):
        skills=data["skills"].split(",")

        data["skills"]=[]

        for skill in skills:
            data["skills"].append(skill.strip())


    if isinstance(data.get("experience_years"),str):
        if data["experience_years"].isdigit():
            data["experience_years"]=int (data["experience_years"])
        
    return data

llm =ScriptedLLM(mock_responses)

profiles=[]
failure=[]

strict_mode="--strict" in sys.argv

for i , resume in enumerate(RESUMES,start=1):
    try:
        prompt=build_prompt(resume)


        response=llm.generate(prompt)
        json_text=extract_json_block(response)

        data=json.loads(json_text)

        if not strict_mode:
            repair_types(data)

        profile= ResumeProfile(**data)

        profiles.append(profile)

        print(f"[{i}/3] {profile.name} OK")
        logger.info(f"Resume {i} extracted successfully")

    except ValidationError as e:
        failure.append(i)

        field=e.errors()[0]["loc"][0] 
        # Take the first validation error and find the field name that caused it.

        print(f"[{i}/3] resume_{i} FAILED -> Misisng/invalid :{field}")
        logger.error(f"Resume {i} failed: {field}")

data=[]
for  p in profiles:
    data.append(p.model_dump())

with open("Extracted_resumes.json","w")as file:
    json.dump(data,file,indent=2)

logger.info("saved profile to extracted_resumes.json")

print(f"Summary: {len(profiles)} extracted,"
    f"{len(failure)} failed of {len(RESUMES)}")

logger.info(f"Summary: {len(profiles)} extracted,"
    f"{len(failure)} failed of {len(RESUMES)}")