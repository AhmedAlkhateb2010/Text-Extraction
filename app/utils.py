#File Path: C:\Users\Msi\Desktop\Text Extraction\app\utils.py

from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from langdetect import detect, LangDetectException
from .config import TESSERACT_PATH

# Preprocess the image for better OCR performance
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
    img = img.filter(ImageFilter.MedianFilter())  # Apply median filter
    return img

# Detect the language of the given text
def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

# Extract text from an image
def extract_text_from_image(image_path):
    try:
        img = preprocess_image(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
