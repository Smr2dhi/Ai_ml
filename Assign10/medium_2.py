import logging
import os
log_file=os.path.join(os.path.dirname(__file__),"prompt.log")



logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger=logging.getLogger(__name__)

def call_llm(prompt):
    """Fake LLM call. Prints the prompt, returns a canned reply.
    Replaced by a real Azure OpenAI call in Session 22.
    """

    print("--- PROMPT SENT TO LLM ---")
    print(prompt)
    print("--- END PROMPT ---")

    return "(model response would appear here)"

def build_prompt(
    role,
    context,
    task,
    constaints,
    output_format,
    examples=None
):
    if not role:
        logger.info("Role not found")
        raise ValueError("Role is required")
    
    if not task:
            logger.info("task not found")
            raise ValueError("task is required")
        
    if not output_format:
            logger.info("output_format not found")
            raise ValueError("output_format is required")
        
    blocks=[]
    
    blocks.append(f"Role: {role}")
    
    if examples:
        example_line=["Examples: "]
        
        for example in examples:
            example_line.append(f"Input: {example['input']}")
    
            example_line.append(f"Output: {example['output']}")

        blocks.append("\n".join(example_line))
    
    blocks.append(f"Task:\n{task}")
    logger.info("Task added")
    
    blocks.append(f"Constraints:\n{constaints}")
    logger.info("Constraints added")

    blocks.append(f"Output Format:\n{output_format}")
    logger.info("Output Format added")

    
    return "\n".join(blocks)


def main():
    role = "You are a support ticket classifier."

    context = None
    task = 'Classify the ticket: "My package arrived with a broken seal."'
    constraints = "Reply with the category name only."
    output_format = "One word: Complaint, Feedback, or Inquiry."

    examples = [
        {
            "input": "Refund not received",
            "output": "Complaint"
        },
        {
            "input": "Great customer service",
            "output": "Feedback"
        }
    ]
    
    
    zero_shot_prompt = build_prompt(
        role,
        context,
        task,
        constraints,
        output_format
    )

    call_llm(zero_shot_prompt)

    few_shot_prompt = build_prompt(
        role,
        context,
        task,
        constraints,
        output_format,
        examples
    )

    call_llm(few_shot_prompt)


if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print("Error:", e)
    