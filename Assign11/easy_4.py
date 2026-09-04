import os
import asyncio
from openai import AsyncOpenAI
from agents import(Agent,Runner,set_default_openai_api,set_default_openai_client,set_tracing_disabled)
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(True)
# os.environ["OPENAI_AGENTS_DISABLE_TRACING"]="true"
api_key=os.getenv("GEMINI_API_KEY")
end_point = os.getenv("GEMINI_ENDPOINT")
model = os.getenv("GEMINI_MODEL")

question="what is api?"

def mock_answer(question):
    print("Mock_answer: ---")
    return "Api is a software intermediary that allow two appliactions to talk to each other"

if not api_key or not end_point:
    print("[NOTICE] GEMINI_API_KEY or GEMINI_ENDPOINT  is not set")

    answer=mock_answer(question)
    print("MODE: mock")
    print(answer)

else:
    async def main():

        client=AsyncOpenAI(
            api_key=api_key,
            base_url=end_point
        )
        set_default_openai_client(client)
        set_default_openai_api("chat_completions")

        agent=Agent(
            name="AI Assistanat",
            instructions="You are useful AI Assistant",
            model=model
        )

        try:
            result=await Runner.run(agent,question)
            answer=result.final_output

            print("Assistant: --")
            print(answer)

            print("Mode:Gemini")
            print("Model requesed:",model)

        except Exception as e:
            print("[NOTICE] Gemini api request failed-using mock response")
            print("Actual error:", e)

            answer=mock_answer(question)
            print("Model:mock")

    asyncio.run(main())