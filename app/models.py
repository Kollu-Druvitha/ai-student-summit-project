from pydantic import BaseModel
from typing import List, Optional

# This is like a blueprint for breach data
class Breach(BaseModel):
    email: str
    breach_name: str
    breach_date: str
    data_leaked: List[str]

# Blueprint for the response we send to frontend
class BreachCheckResponse(BaseModel):
    email: str
    found_in_breaches: bool
    breach_count: int
    breaches: List[Breach]
    risk_level: str  # LOW, MEDIUM, HIGH
    risk_score: int  # 0-100
    ai_advice: str