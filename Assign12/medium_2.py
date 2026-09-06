import json

from Assign12.llmClient import ScriptedLLM

STRICT_REMINDER =""" Your previous reply was not valid JSON.
 Return ONLY a valid JSON object matching the schema — no explanation, no markdown fences. """

def extract_json_block(text):
	start=text.find("{")
	end=text.rfind("}")

	if start!= -1 and end!= -1:
		return text[start:end+1]
	
	return text


def ask_for_json(llm, prompt,required_fields,max_attempts=3):
	for attempt in range(1,max_attempts+1):
		if attempt==1:
			attempt_prompt=prompt

		else:
			attempt_prompt=prompt+STRICT_REMINDER

		response=llm.ask(attempt_prompt)

		try:
			cleaned=extract_json_block(response)
			data=json.loads(cleaned)

			missing_fields=[field for field in required_fields if field not in data]

			if missing_fields:
				print(f"Attempt {attempt}: missing fields {missing_fields}")
				continue

			print(f"Attempt {attempt}: success")
			return data,attempt

		except json.JSONDecodeError as e:
			print(f"Attempt {attempt}: invalid JSON -> {e}")

	raise  ValueError(f"Failed to get valid JSON after {max_attempts} attempts")

		

llm = ScriptedLLM([
	"Hello! How can I help you today? ",

	"""```json
{
	"name":"sam",
	"email" : "sam@gmail"
}
``` """,
"""{
	"name":"sam",
	"email":"sam@gmail.com",
	"phone":"9102344412"
}"""
])

prompt="""
Extract the conatct information

return a json object format like this for data:
{	"name":"",
	"email":"",
	"phone":""
}
"""

required_field=["name","email","phone"]

result,attempt=ask_for_json(llm,prompt,required_field)

print(f"{result}, attempt: {attempt}")


