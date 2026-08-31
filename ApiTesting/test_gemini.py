from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="""
    Tell me about Python.

    Return the answer in this format:

    {
        "topic": "Python",
        "definition": "...",
        "uses": [
            "...",
            "...",
            "..."
        ],
        "difficulty": "..."
    }

    Return only the JSON. Do not add any explanation outside the JSON.
    """
)

print("Gemini Response:")
print(response.text)