from flask import Flask, render_template, request, redirect, url_for, jsonify
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pix_count = 0

def is_fire_color(rgb):
    r, g, b = rgb
    return (180 <= r <= 255) and (60 <= g <= 140) and (0 <= b <= 60)

def check_continuous_fire_color(image_path, min_pixels=2):
    global pix_count, width, height
    img = Image.open(image_path)
    img = img.convert("RGB")
    
    width, height = img.size
    
    # continuous_count = 0 
    for y in range(height):
        continuous_count = 0 
        for x in range(width):
            current_rgb = img.getpixel((x, y))
            
            if is_fire_color(current_rgb):
                continuous_count += 1
                pix_count += 1 
                if continuous_count >= min_pixels:
                    return True
            else:
                continuous_count = 0 
    
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)
        result = check_continuous_fire_color(image_path)

        fire_detected = result
        
        fire_percentage = ((pix_count * 1000) / (width))%100
        
        response = {
            "fire_detected": fire_detected,
            "fire_percentage": fire_percentage
        }
        return jsonify(response)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
