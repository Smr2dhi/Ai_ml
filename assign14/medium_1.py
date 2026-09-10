knowledge = [ 
    {"text": "The employee handbook covers office hours, dress code, and workplace conduct.", 
     "metadata": {"document_name": "Employee Handbook", "category": "HR", "source": "PDF"}}, 
    {"text": "Employees receive 20 days of annual leave. Unused leave can be carried forward up to 10 days.", 
     "metadata": {"document_name": "Leave Policy", "category": "HR", "source": "PDF"}}, 
    {"text": "Travel reimbursement claims must be submitted within 30 days with receipts.", 
     "metadata": {"document_name": "Travel Policy", "category": "Finance", "source": "DOCX"}}, 
    {"text": "Laptops must use disk encryption and lost devices must be reported to the IT helpdesk.", 
     "metadata": {"document_name": "IT Policy", "category": "IT", "source": "Wiki"}}, 
] 



def main():
	while True:
		question=input("Enter your query or 'q' for quit: ")
		if question.lower()=='q':
			break
		

if __name__ =="__main__":
	main()