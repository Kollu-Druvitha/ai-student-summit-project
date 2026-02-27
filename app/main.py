from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import Breach, BreachCheckResponse
from .data_loader import load_breach_data, check_email_in_breaches
from .risk_scorer import calculate_risk_score
from .gemini_helper import generate_ai_advice

# Create FastAPI app
app = FastAPI(
    title="Dark Web Breach Monitor",
    description="Check if your email appears in data breaches",
    version="1.0.0"
)

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load breach data when server starts
print("🔄 Loading breach data...")
breach_data = load_breach_data()
print(f"✅ Loaded {len(breach_data)} breaches")

@app.get("/")
def root():
    """Welcome message"""
    return {
        "message": "Dark Web Breach Monitor API",
        "endpoints": {
            "check_email": "/check/{email}",
            "health": "/health",
            "debug_emails": "/debug/emails"
        }
    }

@app.get("/health")
def health_check():
    """Check if API is running"""
    return {"status": "healthy", "breaches_loaded": len(breach_data)}

@app.get("/check/{email}", response_model=BreachCheckResponse)
def check_email(email: str):
    """
    Check if an email appears in any breaches
    Returns breach info, risk level, and AI advice
    """
    # Find breaches for this email
    found_breaches = check_email_in_breaches(email, breach_data)
    
    # Calculate risk
    risk_level, risk_score = calculate_risk_score(found_breaches)
    
    # Get AI advice
    ai_advice = generate_ai_advice(email, found_breaches, risk_level)
    
    # Prepare response
    response = BreachCheckResponse(
        email=email,
        found_in_breaches=len(found_breaches) > 0,
        breach_count=len(found_breaches),
        breaches=found_breaches,
        risk_level=risk_level,
        risk_score=risk_score,
        ai_advice=ai_advice
    )
    
    return response

# For debugging - show available emails
@app.get("/debug/emails")
def list_emails():
    """Debug endpoint - list all emails in database"""
    emails = list(set([b.email for b in breach_data]))
    return {"emails": emails}