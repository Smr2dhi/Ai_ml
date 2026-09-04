from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

end_point=os.getenv("GEMINI_ENDPOINT")

api_key=os.getenv("GEMINI_API_KEY")
print(api_key)

model=os.getenv("GEMINI_MODEL")
print(model)

question="What is the API ?"

def mock_answer(question):
    return "The capital of india is NEW DELHI."

if not api_key or not end_point:
    print("[NOTICE] GEMINI_API_KEY is not set- using mock reponse")

    answer=mock_answer(question)
    print("Mock answer--",answer)
    

else:
    client= OpenAI(
        api_key=api_key,
        base_url=end_point

    )
    try:
        response=client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role":"system",
                    "content":""" You are a helpful API teacher.
                                    Explain concepts in simple language.
                                    Give a small example when useful.
                                    Keep answers concise."""
                },
                {
                    "role":"user",
                    "content":question
                }
            ]
        )

        answer=response.choices[0].message.content

        print("Assistant- Gemini answer---")
        print(answer)

        print("Model returned:", response.model)
        print("Model requested:", model)



    except Exception as e:
        print("[NOTICE] Gemini API request failed - using MOCK response.")

        answer=mock_answer(question)
        print(answer)
        print("Mode: mock")