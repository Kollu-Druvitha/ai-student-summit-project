from flask import Flask, request, jsonify
from flask_cors import CORS
from breaches import check_breach

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "Dark Web Breach Monitor API Running"}

@app.route("/check-breach", methods=["POST"])
def check_email_breach():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = check_breach(email)
    if result["status"] == "breached":
        result["recommendations"] = [
            "Change your password immediately",
            "Enable Two-Factor Authentication (2FA)",
            "Avoid reusing passwords across sites",
            "Use a trusted password manager"
        ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)