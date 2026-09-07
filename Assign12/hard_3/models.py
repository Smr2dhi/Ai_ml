from pydantic import BaseModel,Field
from typing import List,Optional,Literal

class AutoTagResult(BaseModel): 
    category: Literal["HR", "Finance", "Tech", "General"] 
    tags: List[str] 
 
class DocumentOut(BaseModel): 
    id: int 
    name: str 
    category: Optional[str] 
    tags: List[str] 
 
class AskRequest(BaseModel): 
    question: str 
 
class StructuredAnswer(BaseModel): 
    answer: str 
    sources: List[str] 
    confidence: float = Field(ge=0.0, le=1.0) 