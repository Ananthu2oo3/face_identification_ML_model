from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/classify', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
                

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5432)