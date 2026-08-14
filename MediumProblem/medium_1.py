student={}
 
students=[]
 
numberOfStudent =int(input("No of students? "))
 
 
def averageMarks(marks):
	value=(sum(marks)/len(marks))
	return value
 
 
def grade(avg_marks):
	if avg_marks>=90:
		print("A")
	elif 75<= avg_marks <90:
		print("B")
	elif 60<= avg_marks <75:
		print("C")
	else:
		print("Fail")
 
    	
 
for i in range(numberOfStudent):
	name=input("Enter your name: ")
	subjects=int(input("How many subjects ?"))
 
	marks=[]
	for j in range(subjects):
		value=int(input(f"marks {j+1}: "))
 
		marks.append(value)
	print(marks)
 
	avg_marks = averageMarks(marks)
	print("AvgValue: ",avg_marks)
 
	get_grade = grade(avg_marks) 
 
 
	student[name]=avg_marks
 
topper = max(student)
print("Topper : ",topper)

