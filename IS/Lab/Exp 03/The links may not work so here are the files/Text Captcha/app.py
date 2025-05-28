from flask import Flask, render_template, request, session, jsonify, send_file
import random
import string
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Ensure captcha_images directory exists
CAPTCHA_FOLDER = "captcha_images"
if not os.path.exists(CAPTCHA_FOLDER):
    os.makedirs(CAPTCHA_FOLDER)

# Function to generate a CAPTCHA image
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session["captcha_text"] = captcha_text  # Store the answer in session

    # Create an image
    img = Image.new('RGB', (150, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 30)  # Load font
    except IOError:
        font = ImageFont.load_default()  # Fallback if font not found

    draw.text((20, 10), captcha_text, font=font, fill=(0, 0, 0))  # Add text to image

    # Save the image
    image_path = os.path.join(CAPTCHA_FOLDER, "captcha.png")
    img.save(image_path)

    return image_path

@app.route("/generate_captcha")
def get_captcha():
    captcha_path = generate_captcha()
    return jsonify({"captcha_url": "/captcha_image"})

@app.route("/captcha_image")
def captcha_image():
    return send_file(os.path.join(CAPTCHA_FOLDER, "captcha.png"), mimetype="image/png")

@app.route("/verify_captcha", methods=["POST"])
def verify_captcha():
    user_answer = request.form.get("captcha")
    if user_answer and user_answer.upper() == session.get("captcha_text"):
        return jsonify({"success": True, "message": "CAPTCHA verified!"})
    return jsonify({"success": False, "message": "Invalid CAPTCHA, try again!"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
