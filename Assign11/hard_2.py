
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import asyncio
import logging
from agents import set_tracing_disabled

log_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"hard_2.log"
)

report_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),"cost_report.txt"
)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger=logging.getLogger(__name__)

load_dotenv()
set_tracing_disabled(True)


api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_ENDPOINT")
model=os.getenv("GEMINI_MODEL")

PRICE_PER_1K_INPUT_TOKENS = 0.005
PRICE_PER_1K_OUTPUT_TOKENS = 0.015 

budget=2000

prompts = [
    "What is Python?",
    "What is FastAPI?",
    "How should I prepare for AI engineering?",
    "Explain prompt engineering.",
    "What is an API?",
]


configured=False

if api_key and base_url and model:
    configured=True

client=None

if configured:
    client=AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )


def mock_response(user_prompt):

    logger.info("Mock responses")

    prompt_token = len(user_prompt)
    completion_token = 60
    total_token = prompt_token + completion_token

    usage = {
        "prompt_token": prompt_token,
        "completion_token": completion_token,
        "total_token": total_token
    }
    return "Mock response",usage


async def ask_with_usage(user_prompt):

    if not configured:
        return mock_response(user_prompt)

    logger.info("Calling LLM")

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role":"system",
                "content":"You are an AI agent. Answer in one sentence."
                    },
            {
                "role":"user",
                "content":user_prompt
            }
        ]
    )

    answer=response.choices[0].message.content

    usage_data=response.usage

    input_token=usage_data.prompt_tokens
    output_token=usage_data.completion_tokens
    total_token=usage_data.total_tokens

    usage={
        "prompt_token":input_token,
        "completion_token":output_token,
        "total_token":total_token
    }

    return answer,usage


def calculate_cost(usage):

    input_cost=(usage["prompt_token"]/1000*PRICE_PER_1K_INPUT_TOKENS)

    output_cost=(usage["completion_token"]/1000*PRICE_PER_1K_OUTPUT_TOKENS)

    logger.info("cost calculated")
    return input_cost+output_cost


async def main():

    if not configured:
        print("[NOTICE] env vars are not set-- using mock results")

    total_tokens=0
    failed=0
    skipped=0
    results=[]

    logger.info(f"Processing {len(prompts)} prompts (budget: {budget} tokens)")
    print(f"Processing {len(prompts)} prompts (budget: {budget} tokens)")

    for i ,prompt in enumerate(prompts):

        if total_tokens>=budget:
            print("Total budget spent. skipping remaining prompts")
            skipped=len(prompts)-i
            logger.warning("Skipped remaining prompts")

            break

        try:

            answer,usage=await ask_with_usage(prompt)
            cost=calculate_cost(usage)

            results.append({
                "prompt":prompt,
                "usage":usage,
                "cost":cost

            })
            total_tokens+=usage["total_token"]

        except Exception as e:

            logger.warning("Exception: %s",e)
            print("ERROR: ",e)
            failed+=1

        await asyncio.sleep(1)

    print("---Token and cost-----")

    print(
        "Prompt".ljust(30),
        "Prompt".rjust(7),
        "Compl".rjust(7),
        "Total".rjust(7),
        "Cost($)".rjust(9)
    )

    total_cost=0

    for item in results:

        usage=item["usage"]

        total_cost+=item["cost"]

        print(
            item["prompt"][:30].ljust(30),
            str(usage["prompt_token"]).rjust(7),
            str(usage["completion_token"]).rjust(7),
            str(usage["total_token"]).rjust(7),
            f'{item["cost"]:.4f}'.rjust(9)
        )


    print("\nCalls made    :",len(results))
    print("Calls failed  :",failed)
    print("Calls skipped :",skipped)
    print("Total tokens  :",total_tokens)
    print("Estimated cost:",f"${total_cost:.4f}")

    logger.info(f"Calls made     : {len(results)}")
    logger.info(f"Calls failed   : {failed}")
    logger.info(f"Calls skipped  : {skipped}")
    logger.info(f"Total tokens   : {total_tokens}")
    logger.info(f"Estimated cost : ${total_cost:.4f}")

    report=f"""
    ---Token and cost-----

    Calls made    : {len(results)}
    Calls failed  : {failed}
    Calls skipped : {skipped}
    Total tokens  : {total_tokens}
    Estimated cost: ${total_cost:.4f}
    """

    try:
        with open (report_path,"w")as file:
            file.write(report)

        logger.info("Cost report saved")
    except Exception as e:
        logger.exception("Failed to save cost report")
        print("File error:",e)

if __name__=="__main__":
    asyncio.run(main())

