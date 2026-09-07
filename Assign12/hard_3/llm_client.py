import os
from openai import OpenAI
from utils import logger

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
			logger.info("Gemini configuration missing. Using mock response.")
			return mock_response
		try:
			logger.info("creating gemini client")

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
			logger.info("Gemini request successful")
			return response.choices[0].message.content

		except Exception as e:
			logger.error("Gemini request failed")
			logger.error("Error type: %s", type(e).__name__)
			logger.error("Error message: %s", e)

class ScriptedLLM:
	def __init__(self,responses):
		self.responses=list(responses)

	def ask(self,prompt:str,system:str=DEFAULT_SYSTEM)->str:
		# if llm_available():
		# 	return ask_llm(prompt,system=system)

		if not self.responses: 
			logger.info("No scripted responses available")
			return "{}"
		
		if len(self.responses)>1:
			logger.info("Returning next scripted response")
			return self.responses.pop(0)
		
		logger.info("Returning final scripted response")
		return self.responses[0]