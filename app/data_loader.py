import json
from typing import List
from .models import Breach

def load_breach_data(file_path: str = "data/breaches.json") -> List[Breach]:
    """
    Load breach data from JSON file
    Returns a list of Breach objects
    """
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Convert each dictionary to a Breach object
        breaches = [Breach(**item) for item in data]
        
        print(f"✅ Loaded {len(breaches)} breach records")
        return breaches
    
    except FileNotFoundError:
        print(f"❌ Error: Could not find {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: {file_path} is not valid JSON")
        return []

def check_email_in_breaches(email: str, all_breaches: List[Breach]) -> List[Breach]:
    """
    Find all breaches for a specific email
    """
    matching_breaches = []
    
    for breach in all_breaches:
        if breach.email.lower() == email.lower():  # Case-insensitive check
            matching_breaches.append(breach)
    
    return matching_breaches