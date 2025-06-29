from flask import Blueprint, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from io import BytesIO

json_to_pdf_bp = Blueprint('json_to_pdf', __name__)
@json_to_pdf_bp.route('/convert/json-to-pdf', methods=['POST'])
def convert_json_to_pdf():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    file = request.files['file']
    if not file.filename.endswith('.json'):
        return {'error': 'Only JSON files are allowed'}, 40
    try:
        json_data = json.load(file)
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)
        y = 750
        for key, value in json_data.items():
            c.drawString(50, y, f"{key}: {value}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name='converted.pdf',
            mimetype='application/pdf'
        )
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON file'}, 400
    except Exception as e:
        return {'error': f'Error processing file: {str(e)}'}, 500