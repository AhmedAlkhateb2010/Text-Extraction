# File Path: C:\Users\Msi\Desktop\Text Extraction\app\app.py

from flask import Flask
from .routes import main
from .config import TESSERACT_PATH
import pytesseract
import os

# Set Tesseract environment variables
os.environ['TESSDATA_PREFIX'] = r'C:\Users\Msi\Desktop\Text Extraction\tesseract OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.register_blueprint(main)
    return app
