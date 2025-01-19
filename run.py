# File path: C:\Users\Msi\Desktop\Text Extraction\app.py

import os
import sys

# Add the app directory to the Python path to resolve imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

# Initialize and run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

