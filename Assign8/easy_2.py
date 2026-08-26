SPAM_KEYWORDS = ["free","w1n" , "pr1ze","winner", "prize", "urgent", "lottery"]

def is_spam(subject):
	for keyword in SPAM_KEYWORDS:
		if keyword.lower() in subject.lower():
			return True

	return False

subjects = [ 
    "Meeting moved to 3pm", 
    "You are a WINNER - claim your prize", 
    "Free lottery tickets inside", 
    "Quarterly report attached", 
    "URGENT: verify your account", 
	"W1N A PR1ZE t0day" 
] 

for data in subjects:

	if is_spam(data):
		print("spam? yes",data)

	else:
		print("spam? no :",data)

content="""
1. "W1N A PR1ZE t0day" 
Not Spam
Rule-based verdict is wrong.
ML would learn patterns from thousands
of examples instead of matching fixed keywords.

2. # This is an endless losing game because
 spammers can keep changing their wording, 
so we would have to manually add every new trick.
"""

print(content)