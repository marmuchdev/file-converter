from flask import Flask
from flask_cors import CORS
from .converters.json_to_pdf import json_to_pdf_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    app.register_blueprint(json_to_pdf_bp, url_prefix='/api')
    return app