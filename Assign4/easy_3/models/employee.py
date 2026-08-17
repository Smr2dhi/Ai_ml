class Employee:
    def __init__(self,name,department):
        self.name=name
        self.departement=department

    def Introduce(self):
        return f"Hi I am {self.name} from {self.departement}"