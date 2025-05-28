from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Function to generate a math CAPTCHA
def generate_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    session["captcha_answer"] = num1 + num2  # Store the answer in the session
    return f"{num1} + {num2} = ?"

@app.route("/generate_captcha")
def get_captcha():
    return jsonify({"captcha": generate_captcha()})

@app.route("/verify_captcha", methods=["POST"])
def verify_captcha():
    user_answer = request.form.get("captcha")
    if user_answer and user_answer.isdigit():
        if int(user_answer) == session.get("captcha_answer"):
            return jsonify({"success": True, "message": "CAPTCHA verified!"})
    return jsonify({"success": False, "message": "Invalid CAPTCHA, try again!"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
