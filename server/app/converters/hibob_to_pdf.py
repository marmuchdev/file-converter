from flask import Blueprint, request, send_file, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from lxml import html
import json
import zipfile
import io
import re
import os

hibob_to_pdf_bp = Blueprint('hibob_to_pdf', __name__)
#commetn
def clean_filename(text):
    """Sanitize filename by replacing spaces with underscores and removing invalid characters except parentheses."""
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Remove invalid filename characters except parentheses
    text = re.sub(r'[^\w\s\-\(\)]', '', text).strip()
    return text

def strip_html_tags(html_text):
    """Remove HTML tags and format content."""
    if not html_text:
        return ""
    tree = html.fromstring(html_text)
    text = tree.text_content().strip()
    return text.replace('\n', ' ').replace('\r', '')

@hibob_to_pdf_bp.route('/convert/hibob-to-pdf', methods=['POST'])
def convert_hibob_to_pdf():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    if not file.filename.endswith('.json'):
        return {'error': 'Only JSON files are allowed'}, 400
    
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON file'}, 400

    # Initialize ZIP buffer
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Process manager review
        if data.get('manager'):
            manager = data['manager']
            reviewer = manager['reviewer']
            form = manager['form']
            answers = manager['answerItems']
            generate_pdf(zip_file, reviewer, form, answers)

        # Process peer reviews
        for peer in data.get('peers', []):
            reviewer = peer['reviewer']
            form = peer['form']
            answers = peer['answerItems']
            generate_pdf(zip_file, reviewer, form, answers)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='hibob_reviews.zip'
    )

def generate_pdf(zip_file, reviewer, form, answers):
    """Generate a PDF for a single reviewer and add to ZIP."""
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.black
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceAfter=6
    )

    # Sanitize reviewer name for filename
    reviewer_name = clean_filename(reviewer['displayName'])
    title = clean_filename(form['title'])
    filename = f"{title}_{reviewer_name}.pdf"
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch, bottomMargin=inch/2)
    story = []

    # Add title
    story.append(Paragraph(form['title'], title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Add reviewer name and type
    reviewer_type = reviewer['reviewerType'].capitalize()
    story.append(Paragraph(f"Reviewer: {reviewer['displayName']} ({reviewer_type})", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    # Add submission date
    submission_date = reviewer['modificationDate']
    story.append(Paragraph(f"Date: {submission_date}", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    # Map answers to questions
    question_map = {}
    for item in form['items']:
        if item['type'] == 'category':
            for sub_item in item.get('items', []):
                if sub_item['type'] == 'open_question':
                    question_map[str(sub_item['id'])] = sub_item['title']

    # Add questions and answers
    for answer_item in answers:
        question_id = str(answer_item['questionId'])
        question_text = strip_html_tags(question_map.get(question_id, f"Question ID: {question_id}"))
        answer_text = strip_html_tags(answer_item['answer']['value'])
        
        story.append(Paragraph(f"Question: {question_text}", heading_style))
        story.append(Paragraph(answer_text, body_style))
        story.append(Spacer(1, 0.1 * inch))

    # Build PDF
    doc.build(story)
    zip_file.writestr(filename, buffer.getvalue())