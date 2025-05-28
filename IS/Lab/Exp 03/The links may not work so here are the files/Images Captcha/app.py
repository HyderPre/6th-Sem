from flask import Flask, render_template, request, session, jsonify, send_file
import random
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Ensure captcha_images directory exists
CAPTCHA_FOLDER = "captcha_images"
if not os.path.exists(CAPTCHA_FOLDER):
    os.makedirs(CAPTCHA_FOLDER)

# Define categories and shapes
CAPTCHA_CATEGORIES = {
    "Circle": "circle",
    "Square": "square",
    "Triangle": "triangle"
}

def generate_captcha_images():
    """Generates 9 random images with different shapes and saves them."""
    selected_category = random.choice(list(CAPTCHA_CATEGORIES.keys()))  # Pick a shape type
    correct_shape = CAPTCHA_CATEGORIES[selected_category]  # Shape to identify

    correct_images = []
    all_images = []

    for i in range(9):
        shape_type = correct_shape if i < 3 else random.choice(list(CAPTCHA_CATEGORIES.values()))  # 3 correct, 6 random
        img_name = f"captcha_{i}.png"
        img_path = os.path.join(CAPTCHA_FOLDER, img_name)
        
        # Create image
        img = Image.new("RGB", (100, 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        if shape_type == "circle":
            draw.ellipse((25, 25, 75, 75), fill=(0, 0, 255))  # Blue Circle
        elif shape_type == "square":
            draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))  # Red Square
        elif shape_type == "triangle":
            draw.polygon([(50, 20), (80, 80), (20, 80)], fill=(0, 255, 0))  # Green Triangle

        img.save(img_path)
        all_images.append(img_name)
        if shape_type == correct_shape:
            correct_images.append(img_name)

    session["correct_images"] = correct_images
    session["captcha_category"] = selected_category

    return selected_category, all_images

@app.route("/generate_captcha")
def get_captcha():
    """API to generate CAPTCHA images dynamically."""
    category, images = generate_captcha_images()
    return jsonify({
        "category": category,
        "images": [f"/captcha_images/{img}" for img in images]
    })

@app.route("/captcha_images/<filename>")
def serve_captcha_image(filename):
    """Serves dynamically generated images."""
    return send_file(os.path.join(CAPTCHA_FOLDER, filename), mimetype="image/png")

@app.route("/verify_captcha", methods=["POST"])
def verify_captcha():
    """Validates user-selected images."""
    selected_images = request.json.get("selectedImages", [])
    correct_images = session.get("correct_images", [])

    if set(selected_images) == set([f"/captcha_images/{img}" for img in correct_images]):
        return jsonify({"success": True, "message": "CAPTCHA verified!"})
    return jsonify({"success": False, "message": "Incorrect selection, try again!"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
