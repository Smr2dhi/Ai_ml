from pydantic import BaseModel,Field
from typing import Literal

class IncidentRequest(BaseModel):
     incident_id :int =Field(gt=0)
     description :str=Field(min_length=10)


class IncidentAnalysis(BaseModel):
     category:Literal[ "Application", "Data", "Integration", "Infrastructure",  "Unknown"]

     severity:Literal[ "Low", "Medium", "High"]

     summary:str
     next_action:str
     