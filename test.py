from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import base64
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Read image file
            img_bytes = file.read()
            # Convert image to base64 string
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            return redirect(url_for('uploaded_file', img_base64=img_base64))

@app.route('/uploads/<img_base64>')
def uploaded_file(img_base64):
    # Decode base64 string to image bytes
    img_bytes = base64.b64decode(img_base64)
    # Convert bytes to numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    # Decode numpy array to OpenCV image format
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return "Error: Image not found or could not be opened."

    # Process the image (e.g., apply Haar cascade)
    cropped = haar_cascade(img)
    input = stack(cropped)
    outputs = predict(input)

    # Determine the result based on predictions
    max_idx = np.argmax(outputs)
    celebrities = {
        0: ("scarlett_johansson.jpg", "scarlett_johansson.html"),
        1: ("mark_ruffalo.jpg", "mark_ruffalo.html"),
        2: ("robert_downey_jr.jpg", "rdj.html"),
        3: ("chris_evans.jpg", "chris_evans.html"),
        4: ("chris_hemsworth.jpg", "chris_hemsworth.html")
    }
    
    filename, template = celebrities.get(max_idx, ("unknown.jpg", "unknown.html"))
    
    return render_template(template, filename=filename, num=max_idx, prob=outputs)

if __name__ == '__main__':
    app.run(debug=True)
