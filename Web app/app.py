from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename, safe_join
import os
from check_finder import run_check_finder
from textdetector import run_text_detection  # Import the text detection function
from stampremover import run_stamp_removal
from signatureextractor import run_signature_extraction

app = Flask(__name__)
UPLOAD_FOLDER = './uploaded_images'
OUTPUT_FOLDER = './output_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure the file name
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            check_results_path = run_check_finder(filepath, 'filled', '60%')
            text_results_path = run_text_detection(filepath)  # Run text detection
            # stamp_detection_results_path = run_stamp_detection(filepath)
            stamp_removal_path = run_stamp_removal(filepath)
            signature_extractor_path = run_signature_extraction(filepath)
            
            return render_template('results.html', original_image=filepath, check_results_image=check_results_path, text_results_image=text_results_path,stamp_image=stamp_removal_path, signature_image=signature_extractor_path)
        else:
            return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    filepath = safe_join(OUTPUT_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
