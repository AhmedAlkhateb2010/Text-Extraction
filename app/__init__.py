from flask import Flask
from .routes import main
import os

def create_app():
    app = Flask(__name__, template_folder=r'C:\Users\Msi\Desktop\Text Extraction\templates')

    # Register the blueprint
    app.register_blueprint(main)

    return app
