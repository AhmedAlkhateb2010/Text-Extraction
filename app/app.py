from flask import Flask
from routes import main

# Initialize Flask app
app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Msi\Desktop\Text Extraction\tesseract OCR\tesseract.exe'  # Update this path based on where Tesseract is installed
