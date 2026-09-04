from openai import AsyncOpenAI,OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

base_url=os.getenv("GEMINI_ENDPOINT")

api_key=os.getenv("GEMINI_API_KEY")

model=os.getenv("GEMINI_MODEL")

def ask(system_prompt, user_prompt):

    if not api_key or not base_url:
        print("[NOTICE] congig is missisng using mock responses")

        if "career counselor" in system_prompt.lower():
            return "Career Counselor: Build practical AI projects and keep improving your communication skills."

        if "technical interviewer" in system_prompt.lower():
            return "Technical Interviewer: Practice Python, ML, APIs, and system design."

        else:
            return "Helpful AI Assistant: Learn Python, machine learning, APIs, and build projects."

    
    print("Calling real llm-------")
    client=OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    response=client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_prompt}
        ]
    )
    
    return response.choices[0].message.content

assistant_prompt=( "You are a helpful AI assistant.answer in 5 sentences point wise")
carrer_prompt=( "You are a career counselor. Give practical, encouraging advice.answer in 5 sentences point wise")
interviewer_prompt=("You are a strict technical interviewer. Answer in at most 2 sentences.")

question = "How should I prepare for AI engineering?"

print("---Helpful AI Assitanat---")
print(ask(assistant_prompt,question))

print("---Career Counselor---")
print(ask(carrer_prompt,question))

print("---Strict Technical Interviewer  ---")
print(ask(interviewer_prompt,question))