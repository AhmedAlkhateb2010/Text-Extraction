import pytesseract
from PIL import Image
from langdetect import detect
import os
import pandas as pd

def process_file(file_path):
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
        language_column.append(detect(line_text))  # Detect language
        word_count_column.append(len(line_text.split()))  # Word count
        character_count_column.append(len(line_text))  # Character count
        coordinates_column.append(f"({coordinates[0]}, {coordinates[1]})")  # Coordinates
    
    return text_column, language_column, word_count_column, character_count_column, coordinates_column

def save_to_excel(output_filename, text_column, language_column, word_count_column, character_count_column, coordinates_column):
    # Create a DataFrame for the extracted data
    df = pd.DataFrame({
        "Text": text_column,
        "Language": language_column,
        "Word Count": word_count_column,
        "Character Count": character_count_column,
        "Coordinates": coordinates_column
    })
    
    # Save DataFrame to Excel
    output_filepath = os.path.join(r'C:\Users\Msi\Desktop\Text Extraction\app\uploads', output_filename)  # Raw string for file path
    df.to_excel(output_filepath, index=False, engine='openpyxl')
    return output_filepath
