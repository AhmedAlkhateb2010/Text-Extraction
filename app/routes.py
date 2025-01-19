# File Path: C:\Users\Msi\Desktop\Text Extraction\app\routes.py

from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pytesseract
from .utils import extract_text_from_image
from .process import process_file_and_save
from .config import TESSERACT_PATH

# Set Tesseract environment variables
os.environ['TESSDATA_PREFIX'] = r'C:\Users\Msi\Desktop\Text Extraction\tesseract OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

main = Blueprint('main', __name__)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heif', 'heic', 'raw', 'cr2', 'nef', 'dng', 'svg', 'eps', 'ai', 'ico', 'pdf'}
UPLOAD_FOLDER = r'C:\Users\Msi\Desktop\Text Extraction\app\uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        try:
            output_filename = f"extracted_text_{filename.split('.')[0]}.xlsx"
            output_filepath = process_file_and_save(file_path, output_filename)
            return jsonify({"download_link": output_filepath})
        except Exception as e:
            return jsonify({'error': f'Error processing the file: {str(e)}'}), 500
    return jsonify({'error': 'Invalid file type'}), 400