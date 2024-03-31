from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ImageConverter:
    def convert_to_black_and_white(self, input_image_path, output_image_path):
        try:
            # Open the input image
            image = Image.open(input_image_path)
            
            # Convert the image to grayscale
            bw_image = image.convert("L")
            
            # Save the black and white image
            bw_image.save(output_image_path)
            return True
        except Exception as e:
            print("An error occurred:", e)
            return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            converter = ImageConverter()
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'bw_' + filename)
            if converter.convert_to_black_and_white(filepath, output_filepath):
                return redirect(url_for('uploaded_file', filename='bw_' + filename))
            else:
                return "Error occurred during conversion"
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
