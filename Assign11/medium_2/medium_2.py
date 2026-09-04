from Assign11.medium_2.ai_client import AIClient,logger
from agents import Agent,Runner
import asyncio

async def main():
    client=AIClient()
    agent=client.agent

    questions=[
        "What is ai?",
        "what is 2+2?",
        "what is prime number"

    ]
    for ques in questions:
        print("Ques. ",ques)

        if client.mode=="mock":
            answer=await client.generate_response(ques)

            input_tokens = 25
            output_tokens = 40
            total_tokens = 65

        else:


            answer= await Runner.run(agent,ques)
            print("Answer: ",answer.final_output)

            usage=answer.context_wrapper.usage
            input_tokens = usage.input_tokens
            output_tokens = usage.output_tokens
            total_tokens = usage.total_tokens

        logger.info(
            "Ques:%s | Input_token: %s | Output_token: %s | Total_token: %s",
            ques,
            input_tokens,
            output_tokens,
            total_tokens
        )

        print("Input tokens:", usage.input_tokens)
        print("Output tokens:", usage.output_tokens)
        print("Total tokens:", usage.total_tokens)


asyncio.run(main())