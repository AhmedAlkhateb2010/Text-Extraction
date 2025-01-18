from flask import Blueprint, request, jsonify, send_from_directory, render_template, url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
from langdetect import detect, LangDetectException
import pandas as pd

# Update to your local Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Msi\Desktop\Text Extraction\tesseract OCR\tesseract.exe'

# Blueprint setup
main = Blueprint('main', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the index page (upload form)
@main.route('/')
def index():
    return render_template('index.html')  # Just the filename


# Route for file upload (POST method)
@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(r'C:\Users\Msi\Desktop\Text Extraction\app\uploads', filename)  # Raw string for file path
        file.save(file_path)

        # Open the image for text extraction
        img = Image.open(file_path)

        # Extract text and coordinates with pytesseract
        d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        extracted_data = []
        for i in range(len(d['text'])):
            text = d['text'][i]
            if text.strip():  # Ignore empty strings
                x = d['left'][i]
                y = d['top'][i]
                extracted_data.append((text, (x, y)))
        
        # Prepare data for Excel creation
        text_column = []
        language_column = []
        word_count_column = []
        character_count_column = []
        coordinates_column = []

        for line_text, coordinates in extracted_data:
            text_column.append(line_text)
            language_column.append(safe_detect(line_text))  # Detect language using safe_detect
            word_count_column.append(len(line_text.split()))  # Word count
            character_count_column.append(len(line_text))  # Character count
            coordinates_column.append(f"({coordinates[0]}, {coordinates[1]})")  # Coordinates
        
        # Create an Excel file with the extracted data
        output_filename = f"{os.path.splitext(filename)[0]}_extracted.xlsx"
        output_filepath = os.path.join(r'C:\Users\Msi\Desktop\Text Extraction\app\uploads', output_filename)  # Raw string for file path

        # Create a DataFrame for the extracted data
        df = pd.DataFrame({
            "Text": text_column,
            "Language": language_column,
            "Word Count": word_count_column,
            "Character Count": character_count_column,
            "Coordinates": coordinates_column
        })
        
        # Write the DataFrame to Excel
        df.to_excel(output_filepath, index=False, engine='openpyxl')

        # Return a downloadable link for the Excel file
        return jsonify({
            "message": "File successfully uploaded and processed",
            "download_link": url_for('main.download_file', filename=os.path.basename(output_filepath))
        })

    else:
        return jsonify({"error": "Invalid file type"}), 400

# Route for downloading the processed Excel file
@main.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(r'C:\Users\Msi\Desktop\Text Extraction\app\uploads', filename, as_attachment=True)  # Raw string for file path

# Define the safe_detect function to handle empty or invalid text
def safe_detect(text):
    if not text.strip():  # Check if text is empty or just whitespace
        return "Unknown"  # You can return a default language or handle it differently
    try:
        return detect(text)
    except LangDetectException:
        return "Unknown"  # Handle the case where language detection fails
