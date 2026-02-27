# breaches.py
demo_breaches = {
    "test@gmail.com": [
        {"breach": "LinkedIn", "year": 2016, "leaked_data": ["Email", "Password"]}
    ],
    "admin@gmail.com": [
        {"breach": "Adobe", "year": 2013, "leaked_data": ["Email"]}
    ]
}

def check_breach(email):
    email = email.lower().strip()
    if email in demo_breaches:
        return {"status": "breached", "details": demo_breaches[email], "risk_level": "High"}
    return {"status": "safe", "details": [], "risk_level": "Low"}