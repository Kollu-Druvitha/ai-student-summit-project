from typing import List
from .models import Breach

def calculate_risk_score(breaches: List[Breach]) -> tuple[str, int]:
    """
    Calculate risk score based on:
    - Number of breaches
    - Types of data leaked
    """
    if not breaches:
        return "LOW", 0
    
    base_score = 20  # Starting score for any breach
    sensitive_data_weights = {
        "password": 15,
        "credit_card": 25,
        "ssn": 30,  # Social Security Number
        "address": 10,
        "phone": 8,
        "email": 5
    }
    
    total_score = base_score
    
    # Add points based on number of breaches
    breach_count_bonus = len(breaches) * 10
    total_score += breach_count_bonus
    
    # Add points based on sensitive data leaked
    for breach in breaches:
        for data_type in breach.data_leaked:
            data_type_lower = data_type.lower()
            if data_type_lower in sensitive_data_weights:
                total_score += sensitive_data_weights[data_type_lower]
    
    # Cap at 100
    total_score = min(total_score, 100)
    
    # Determine risk level
    if total_score < 30:
        risk_level = "LOW"
    elif total_score < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    return risk_level, total_score