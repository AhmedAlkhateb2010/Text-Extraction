from flask import Blueprint, request, render_template, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from langdetect import detect, LangDetectException
import pandas as pd
from pdf2image import convert_from_path
from flask import Flask, render_template

# Tesseract setup (update this to your local installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Msi\Desktop\Text Extraction\tesseract OCR\tesseract.exe'

# Blueprint setup
main = Blueprint('main', __name__)


# Allowed file extensions (image and PDF)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heif', 'heic', 'raw', 'cr2', 'nef', 'dng', 'svg', 'eps', 'ai', 'ico', 'pdf'}
UPLOAD_FOLDER = r'C:\Users\Msi\Desktop\Text Extraction\app\uploads'

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET'])
def index():
    """Render the index page."""
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and process them."""
    if 'file' not in request.files:
        return render_template('index.html', error="No file selected")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No file selected")

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process the file
        if filename.lower().endswith('.pdf'):
            # Convert PDF to images and extract text from each page
            pages = convert_from_path(file_path, 300)
            extracted_data = []
            for page_number, page in enumerate(pages):
                page_path = f"{file_path}_page_{page_number + 1}.jpg"
                page.save(page_path, 'JPEG')
                extracted_data.extend(extract_text_from_image(page_path))
        else:
            # Extract text from the image file directly
            extracted_data = extract_text_from_image(file_path)

        # Prepare extracted data for Excel
        text_column = []
        language_column = []
        word_count_column = []
        character_count_column = []
        coordinates_column = []

        for line_text, coordinates in extracted_data:
            text_column.append(line_text)
            language_column.append(safe_detect(line_text))
            word_count_column.append(len(line_text.split()))
            character_count_column.append(len(line_text))
            coordinates_column.append(f"({coordinates[0]}, {coordinates[1]})")

        # Create an Excel file
        output_filename = f"{os.path.splitext(filename)[0]}_extracted.xlsx"
        output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)
        df = pd.DataFrame({
            "Text": text_column,
            "Language": language_column,
            "Word Count": word_count_column,
            "Character Count": character_count_column,
            "Coordinates": coordinates_column
        })
        df.to_excel(output_filepath, index=False, engine='openpyxl')

        # Return a download link to the processed file
        return render_template('index.html', download_link=url_for('main.download_file', filename=output_filename))

    return render_template('index.html', error="Invalid file type")

@main.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """Serve the processed file for download."""
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract."""
    img = Image.open(image_path)
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    extracted_data = []
    for i in range(len(d['text'])):
        text = d['text'][i]
        if text.strip():
            x, y = d['left'][i], d['top'][i]
            extracted_data.append((text, (x, y)))
    return extracted_data

def safe_detect(text):
    """Safely detect the language of a given text."""
    if not text.strip():
        return "Unknown"
    try:
        return detect(text)
    except LangDetectException:
        return "Unknown"
