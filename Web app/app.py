from flask import Flask, render_template, request, send_file, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            # Your script functions need to be properly imported and adapted to your actual implementations
            check_results = run_check_finder(filepath, 'filled', 25)
            stamp_results = detect_stamp(filepath)
            signature_results = extract_signature(filepath)
            text_results = detect_text(filepath)

            return render_template('results.html', image_path=filepath, check_results=check_results,
                                   stamp_results=stamp_results, signature_results=signature_results,
                                   text_results=text_results)
        else:
            return redirect(request.url)
    return render_template('home.html')


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
