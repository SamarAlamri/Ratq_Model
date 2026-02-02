# server.py
# Install these first: pip install flask flask-cors requests opencv-python numpy

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import urllib.request
import tensorflow as tf

app = Flask(__name__)
CORS(app) # Allows your Flutter app to talk to this server

erythema_model = tf.keras.models.load_model("erythema_model_finetuned.h5")

def run_ai_model(image_array):
    
    IMG_SIZE = (224, 224) 
    THRESHOLD = 0.25
    resized = cv2.resize(image_array, IMG_SIZE)
    normalized = resized / 255.0
    
    # Add Batch Dimension (e.g. 224,224,3 -> 1,224,224,3)
    batch_input = np.expand_dims(normalized, axis=0)
    
    # 2. Predict
    predictions = erythema_model.predict(batch_input, verbose=0)
    infection_probability = predictions[0][0]

    if infection_probability > THRESHOLD:
        return {
        "erythema": 1, # Replace with actual result
        "exudate": None,    # Replace with actual result
        }
    else:
        return {
        "erythema": 0, # Replace with actual result
        "exudate": None,    # Replace with actual result
        }
    
    
    # ---------------------------------------------------------

@app.route('/analyze', methods=['POST'])
def analyze_wound():
    try:
        data = request.json
        image_url = data.get('imageUrl')

        if not image_url:
            return jsonify({"error": "No URL provided"}), 400

        # 1. Download the image from Cloudinary to memory
        resp = urllib.request.urlopen(image_url)
        image_array = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # 2. Run your model
        results = run_ai_model(image)

        # 3. Send results back to Flutter
        return jsonify(results)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)