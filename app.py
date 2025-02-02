from flask import Flask, request, jsonify
import requests
from io import BytesIO
from PIL import Image
from collections import Counter

app = Flask(__name__)

def get_dominant_color(image_url):
    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Open the image
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")  # Convert to RGB mode
        
        # Resize image to speed up processing
        img = img.resize((100, 100))
        
        # Get colors and their frequency
        pixels = list(img.getdata())
        color_counts = Counter(pixels)
        
        # Get the most common color
        dominant_color = color_counts.most_common(1)[0][0]
        
        # Convert to hex format
        hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)
        return hex_color

    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Image Dominant Color API!"})

@app.route('/dominant-color', methods=['GET'])
def dominant_color_api():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "Missing image URL"}), 400

    color = get_dominant_color(image_url)
    return jsonify({"dominant_color": color})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
