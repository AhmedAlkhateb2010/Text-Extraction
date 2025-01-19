# File Path: C:\Users\Msi\Desktop\Text Extraction\app\process.py

import os
import pandas as pd
from langdetect import detect
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


def process_file(file_path):
    # Ensure file_path is a raw string or use double backslashes
    file_path = file_path.replace("\\", "/")  # Converts backslashes to forward slashes if needed

    # Check if the file is a PDF
    if file_path.lower().endswith('.pdf'):
        try:
            # Convert PDF pages to images
            images = convert_from_path(file_path, 300)  # Set DPI to 300 for better quality
            all_extracted_data = []
            for i, img in enumerate(images):
                # Save the first page as an image (optional step for debugging)
                if i == 0:
                    img.save(f"{file_path}_page_{i+1}.png", 'PNG')

                # Process the image and extract text
                d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                for j in range(len(d['text'])):
                    text = d['text'][j]
                    if text.strip():
                        x = d['left'][j]
                        y = d['top'][j]
                        all_extracted_data.append((text, (x, y)))

            return all_extracted_data
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
    
    # If the file is an image (jpg, png, etc.)
    elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
        img = Image.open(file_path)
        d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        extracted_data = []
        for i in range(len(d['text'])):
            text = d['text'][i]
            if text.strip():
                x = d['left'][i]
                y = d['top'][i]
                extracted_data.append((text, (x, y)))
        return extracted_data
    else:
        raise ValueError("Unsupported file type. Please upload an image or a PDF.")

def process_file_and_save(image_path, output_filename):
    extracted_data = process_file(image_path)
    data = {
        "Text": [],
        "Language": [],
        "Word Count": [],
        "Character Count": [],
        "Coordinates": []
    }

    for text, (x, y) in extracted_data:
        data["Text"].append(text)
        data["Language"].append(detect(text))
        data["Word Count"].append(len(text.split()))
        data["Character Count"].append(len(text))
        data["Coordinates"].append(f"({x}, {y})")

    output_filepath = os.path.join(r'C:\Users\Msi\Desktop\Text Extraction\app\uploads', output_filename)
    pd.DataFrame(data).to_excel(output_filepath, index=False, engine='openpyxl')
    return output_filepath



def process_file(file_path):
    # Ensure file_path is a raw string or use double backslashes
    file_path = file_path.replace("\\", "/")  # Converts backslashes to forward slashes if needed

    # Specify the Poppler path manually if it's not in the PATH
    poppler_path = r'C:\Users\Msi\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin'

    # Check if the file is a PDF
    if file_path.lower().endswith('.pdf'):
        try:
            # Convert PDF pages to images with Poppler path specified
            images = convert_from_path(file_path, 300, poppler_path=poppler_path)
            
            all_extracted_data = []
            for i, img in enumerate(images):
                # Save the first page as an image (optional step for debugging)
                if i == 0:
                    img.save(f"{file_path}_page_{i+1}.png", 'PNG')

                # Process the image and extract text
                d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                for j in range(len(d['text'])):
                    text = d['text'][j]
                    if text.strip():
                        x = d['left'][j]
                        y = d['top'][j]
                        all_extracted_data.append((text, (x, y)))

            return all_extracted_data
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
    
    # If the file is an image (jpg, png, etc.)
    elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):  
        img = Image.open(file_path)
        d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        extracted_data = []
        for i in range(len(d['text'])):
            text = d['text'][i]
            if text.strip():
                x = d['left'][i]
                y = d['top'][i]
                extracted_data.append((text, (x, y)))
        return extracted_data
    else:
        raise ValueError("Unsupported file type. Please upload an image or a PDF.")
