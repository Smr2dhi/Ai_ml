class Employee:
    def __init__(self,name,department):
        self.name= name
        self.department =department

    def introduce(self):
        return f"Hello I am {self.name} form {self.department}"
