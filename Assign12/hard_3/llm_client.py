import os
from openai import OpenAI

try:
	from dotenv import load_dotenv
	load_dotenv()

except ImportError:
	pass

DEFAULT_SYSTEM = (
    "You are a careful assistant that follows output-format "
    "instructions exactly."
)

def llm_available()-> bool:
	return bool(
		os.getenv("GEMINI_API_KEY")
		and os.getenv("GEMINI_ENDPOINT") 
		and os.getenv("GEMINI_MODEL")
	)
def mode()-> str:
	return "Live" if llm_available() else "mock"

def ask_llm(prompt:str,
			 mock_response:str="{}",
			system:str=DEFAULT_SYSTEM
		)->str:

		if not llm_available():
			return mock_response

		client=OpenAI(
			api_key=os.getenv("GEMINI_API_KEY"),
			base_url=os.getenv("GEMINI_ENDPOINT"),
		)
		response= client.chat.completions.create(
			model=os.getenv("GEMINI_MODEL"),
			messages=[
				 {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt
            },
			]
		)
		return response.choices[0].message.content

class ScriptedLLM:
	def __init__(self,responses):
		self.responses=list(responses)

	def ask(self,prompt:str,system:str=DEFAULT_SYSTEM)->str:
		# if llm_available():
		# 	return ask_llm(prompt,system=system)

		if not self.responses:
			return "{}"
		
		if len(self.responses)>1:
			return self.responses.pop(0)
		
		return self.responses[0]