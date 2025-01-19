# File Path C:\Users\Msi\Desktop\Text Extraction\app\__init__.py

from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.register_blueprint(main)
    return app
