class policy:
    def __init__(self,policy_num,premium):
        self.policy_num=policy_num
        self.premium=premium

        def describe(self):
            print("Policy number: ",self.policy_num)
            print("Premium: ",self.premium)

class lifePolicy(policy):
        def __init__(self, policy_num, premium,nominee):
             super().__init__(policy_num, premium)
             self.nominee=nominee

        def describe(self):
            print(self.policy_num,"for",self.nominee)
        
class VechilePolicy(policy):
    def __init__(self, policy_num, premium,num_plate):
          super().__init__(policy_num,premium)
          self.num_plate=num_plate
        
    def describe(self):
        print(self.policy_num, "for" ,self.num_plate)


        
class policyHolder:
    def __init__(self,name,):
        self.name=name
        self.policies=[]
    

    def add_policy(self,policy):
        self.policies.append(policy)
        print("added" ,policy.policy_num,"for",self.name)
    

    def total_premium(self):
        total=0
        for policy in self.policies:
            total+=policy.premium
        print(total)
    
    def show_portfolio(self):
        print(self.name)
        for policy in self.policies:
            policy.describe()
        self.total_premium()


      

holder=policyHolder("sam")
life=lifePolicy(101,5000,"Samriddhi")
vechile=VechilePolicy(103,7000,"up32")

holder.add_policy(life)
holder.add_policy(vechile)

holder.show_portfolio()