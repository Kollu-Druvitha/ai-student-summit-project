import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List
from .models import Breach

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_ai_advice(email: str, breaches: List[Breach], risk_level: str) -> str:
    """
    Use Gemini AI to generate personalized security advice
    """
    try:
        # If no API key, return simple advice
        if not GEMINI_API_KEY:
            return get_fallback_advice(risk_level)
        
        # Prepare information about breaches
        if breaches:
            breach_info = "\n".join([
                f"- {b.breach_name} ({b.breach_date}): Leaked {', '.join(b.data_leaked)}"
                for b in breaches
            ])
        else:
            breach_info = "No breaches found"
        
        # Create prompt for Gemini
        prompt = f"""
        You are a cybersecurity expert. A user's email ({email}) has been checked for data breaches.
        
        Risk Level: {risk_level}
        Breaches found: {len(breaches)}
        
        Details:
        {breach_info}
        
        Provide concise, actionable cybersecurity advice (3-4 sentences) including:
        1. What this means for their security
        2. Immediate steps to take
        3. Long-term security practices
        
        Keep it friendly and helpful for a non-technical user.
        """
        
        # Use Gemini model
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        return get_fallback_advice(risk_level)

def get_fallback_advice(risk_level: str) -> str:
    """Simple advice when AI isn't available"""
    if risk_level == "HIGH":
        return "⚠️ Your email appears in multiple serious breaches. Change passwords immediately, enable 2-factor authentication everywhere, and monitor your accounts for suspicious activity."
    elif risk_level == "MEDIUM":
        return "🟡 Some of your data was found in breaches. Change passwords for affected accounts and consider using a password manager."
    else:
        return "✅ No major issues found. Continue practicing good security habits: unique passwords, 2FA, and regular monitoring."