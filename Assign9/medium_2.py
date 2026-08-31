def call_llm(prompt):
    """FAKE LLM for practice. Returns canned responses - no API, no key, no network.

    In a later session this function will be replaced by a real LLM API call."""

    prompt_lower = prompt.lower()

    if "summarize" in prompt_lower:
        return "SUMMARY: The document describes company policy in three key points."

    if "json" in prompt_lower:
        return '{"answer": "This is a canned JSON response from the fake LLM."}'

    if "do not have enough information" in prompt_lower or "provided" in prompt_lower:
        return "Based on the provided documents: employees receive 18 days of annual leave."

    return "This is a canned response from the fake LLM stub."


def list_placeholder(template):
    placeholders = set()

    start = 0

    while True:
        start_brace = template.find("{", start)

        if start_brace == -1:
            break

        end_brace = template.find("}", start_brace)

        if end_brace == -1:
            break

        name = template[start_brace + 1:end_brace]
        placeholders.add(name)

        start = end_brace + 1

    return placeholders


def fill_template(template, values):
    placeholders = list_placeholder(template)

    # Check missing placeholders
    for placeholder in placeholders:
        if placeholder not in values:
            raise ValueError(
                f"Missing value for placeholder {{{placeholder}}}"
            )

    # Check extra keys
    extra_keys = []

    for key in values:
        if key not in placeholders:
            extra_keys.append(key)

    if extra_keys:
        raise ValueError(
            f"unused keys provided: {extra_keys}"
        )

    # Replace placeholders
    filled_template = template

    for key in values:
        filled_template = filled_template.replace(
            "{" + key + "}",
            str(values[key])
        )

    return filled_template

SUMMARIZE_TEMPLATE = """You are a document summarization assistant.
Summarize the document below in {bullet_count} bullet points.
Use concise business language. Do not invent information.

Document:
{document}"""

POLICY_TEMPLATE = """You are an HR assistant.

Answer the employee's question using only the policy provided.

Question:
{question}

Policy:
{document}"""

def main():

    document = "Employees get 18 days of annual leave. Unused leave lapses in December."

    values = {
        "bullet_count": "3",
        "document": document
    }

    # Fill and print prompt
    prompt = fill_template(SUMMARIZE_TEMPLATE, values)

    print("--- Filled prompt ---")
    print(prompt)

    # Fake LLM response
    print("\n--- Fake LLM response ---")
    print(call_llm(prompt))

    # Missing key error
    try:
        fill_template(SUMMARIZE_TEMPLATE, {
            "bullet_count": "3"
        })
    except ValueError as error:
        print("\nError caught:", error)

    # Extra key error
    try:
        fill_template(SUMMARIZE_TEMPLATE, {
            "bullet_count": "3",
            "document": document,
            "bullet_cont": "3"
        })
    except ValueError as error:
        print("Error caught:", error)

if __name__ == "__main__":
    main()