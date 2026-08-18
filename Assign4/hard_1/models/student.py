class Student:
    def __init__(self,name,roll,marks):
        self.name=name
        self.roll=roll
        self.marks=marks

    def to_dict(self):
        document_details={
            "name":self.name,
            "roll":self.roll,
            "marks":self.marks
        }

        return document_details

def student_from_dict(data):
    s1=Student(
        data["name"],
        int(data["roll"]),
        float(data["marks"])
        )
    return s1