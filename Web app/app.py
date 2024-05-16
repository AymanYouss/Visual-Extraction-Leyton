from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename, safe_join
import os
from check_finder import run_check_finder

app = Flask(__name__)
UPLOAD_FOLDER = './uploaded_images'
OUTPUT_FOLDER = './output_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure the file name
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            check_results_path = run_check_finder(filepath, 'filled', '25%')
            return render_template('results.html', original_image=filepath, check_results_image=check_results_path)
        else:
            return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    filepath = safe_join(OUTPUT_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)
