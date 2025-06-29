import pytest
from app import create_app
from io import BytesIO
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_json_to_pdf_success(client):
    # Create a sample JSON file
    json_data = {"name": "John", "age": 30}
    file_data = BytesIO(json.dumps(json_data).encode('utf-8'))
    file_data.name = 'test.json'
    # Send POST request
    response = client.post(
        '/api/convert/json-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.json')}
    )
    # Assertions
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'
    assert response.headers['Content-Disposition'].startswith('attachment; filename=converted.pdf')

def test_json_to_pdf_no_file(client):
    response = client.post('/api/convert/json-to-pdf')
    assert response.status_code == 400
    assert response.json == {'error': 'No file provided'}

def test_json_to_pdf_invalid_file(client):
    file_data = BytesIO(b"not a json file")
    file_data.name = 'test.txt'
    response = client.post(
        '/api/convert/json-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.txt')}
    )
    assert response.status_code == 400
    assert response.json == {'error': 'Only JSON files are allowed'}

def test_json_to_pdf_invalid_json(client):
    file_data = BytesIO(b"{invalid json}")
    file_data.name = 'test.json'
    response = client.post(
        '/api/convert/json-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.json')}
    )
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid JSON file'}