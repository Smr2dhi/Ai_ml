import os
import asyncio
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner, 
    set_default_openai_client,
    set_default_openai_api,
)
 
#----------------------------------------------------------------------------
 
# 1. Disable telemetry to prevent 401 errors to OpenAI's server
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "true"
 
# 2. Tell the SDK to use the /chat/completions schema instead of /responses
set_default_openai_api("chat_completions")
 
# 3. Use Google's OpenAI-compatible base URL directly
gemini_client = AsyncOpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)
set_default_openai_client(gemini_client, use_for_tracing=False)
 
#----------------------------------------------------------------------------
 
# 4. Use standard Gemini model names (without prefixes like "gemini/")
history_tutor = Agent(
    name="History tutor",
    handoff_description="Specialist for history questions.",
    instructions="Answer history questions clearly and concisely.",
    model="gemini-3.6-flash",
)
 
math_tutor = Agent(
    name="Math tutor",
    handoff_description="Specialist for math questions.",
    instructions="Explain math step by step and include worked examples.",
    model="gemini-3.6-flash",
)
 
triage_agent = Agent(
    name="Homework triage",
    instructions="Route each homework question to the right specialist.",
    handoffs=[history_tutor, math_tutor],
    model="gemini-3.6-flash",
)
 
 
async def main() -> None:
    result = await Runner.run(
        triage_agent,
        "what is 2+2? in 5 points",
    )
    print(result.final_output)
    print(f"Handled by: {result.last_agent}")
 
 
if __name__ == "__main__":
    asyncio.run(main())
 