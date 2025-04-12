from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
import img2pdf
from PIL import Image

app = Flask(__name__)

# Folder setup for uploaded files
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')

    image_paths = []
    for image in images:
        filename = secure_filename(image.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(path)

        img = Image.open(path)
        img = img.convert('RGB')  # Ensure image is in RGB mode
        image_paths.append(path)

    # Convert images to PDF
    pdf_path = os.path.join(OUTPUT_FOLDER, "converted.pdf")
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
