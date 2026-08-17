class Student:
    def __init__(self,name,branch):
        self.name=name
        self.branch=branch


    def introduce(self):
        return f"Hi, I am {self.name} from {self.branch}"


    def to_dict(self):
        return print("name: ",self.name, "branch: ",self.branch)