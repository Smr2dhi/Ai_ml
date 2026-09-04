import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import(
    Agent,
    Runner,
    set_default_openai_api,
    ModelSettings,
    set_default_openai_client,
    set_tracing_disabled
)

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_ENDPOINT")
model=os.getenv("GEMINI_MODEL")
if api_key and base_url:
    client=AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
        )

    set_default_openai_client(client)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)

async def ask(user_prompt,temparature):
    if not api_key or not base_url:
        return {
            "message": "not config env, using mock answer",
            "usage": {
                "prompt_tokens": 25,
                "completion_tokens": 40,
                "total_tokens": 65
            }
        }

  
    
    agent=Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
        model_settings=ModelSettings(
            temparature=temparature
        )
    )
    result=await Runner.run(agent,user_prompt)
    usage=result.context.usage

    print(result)
    print("------------------------------------------------")
    return(
        result.final_output,
        
        {
            "prompt_tokens":usage.input_tokens,
            "completion_tokens":usage.output_tokens,
            "total_tokens":usage.total_tokens
        }
    )

async def main():
    prompt=("Write a one-sentence tagline for an internal "
        "AI Knowledge Assistant.")

    temperatures=[0.0,1.0,1.0]

    for temp in temperatures:
        answer,usage=await ask(prompt,temp)

        print("Temperature:",temp)
        print("Answer: ",answer)

        print(
            f"prompt_tokens={usage['prompt_tokens']}"
            f"completion={usage['completion_tokens']} "
            f"total={usage['total_tokens']}"
        )
asyncio.run(main())