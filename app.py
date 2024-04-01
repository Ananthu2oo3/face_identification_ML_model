from flask import Flask, render_template, request, redirect, url_for
from util import *
import os

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
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(img_path)
    
    if img is None:
        return "Error: Image not found or could not be opened."

    dwt = w2d(img)
    x = stack(dwt)
    y = predict(x)

    if y == 0:
        output = "scarlett_johansson.jpg"
    elif y == 1:
        output = "mark_ruffalo.jpg"
    elif y == 2:
        output = "robert_downey_jr.jpg"
    elif y == 3:
        output = "chris_evans.jpg"
    elif y == 4:
        output = "chris_hemsworth.jpg"

    return render_template('display_image.html', filename=output)

if __name__ == '__main__':
    app.run(debug=True)