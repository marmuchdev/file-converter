import pytest
from app import create_app
from io import BytesIO
import json
import zipfile

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hibob_to_pdf_success(client):
    # Sample HiBob JSON
    hibob_data = {
        "manager": {
            "reviewer": {
                "displayName": "John Smith",
                "reviewerType": "manager",
                "modificationDate": "2024-12-22"
            },
            "form": {
                "title": "December 2024 Three Month Check-in (Manager Review)",
                "items": [
                    {
                        "type": "category",
                        "items": [
                            {"type": "open_question", "id": "17467718", "title": "Summarise performance"}
                        ]
                    }
                ]
            },
            "answerItems": [
                {"questionId": "17467718", "answer": {"value": "Great performance"}}
            ]
        },
        "peers": [
            {
                "reviewer": {
                    "displayName": "Georgina Johnson",
                    "reviewerType": "peer",
                    "modificationDate": "2024-11-19"
                },
                "form": {
                    "title": "December 2024 Three Month Check-in (Peer Review)",
                    "items": [
                        {
                            "type": "category",
                            "items": [
                                {"type": "open_question", "id": "17467720", "title": "Experience working"}
                            ]
                        }
                    ]
                },
                "answerItems": [
                    {"questionId": "17467720", "answer": {"value": "Positive experience"}}
                ]
            }
        ]
    }
    file_data = BytesIO(json.dumps(hibob_data).encode('utf-8'))
    file_data.name = 'test.json'

    response = client.post(
        '/api/convert/hibob-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.json')}
    )

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'
    assert response.headers['Content-Disposition'].startswith('attachment; filename=hibob_reviews.zip')

    # Verify ZIP contents
    zip_buffer = BytesIO(response.data)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        assert len(zip_file.namelist()) == 2
        assert 'December_2024_Three_Month_Check-in_(Manager_Review)_John_Smith.pdf' in zip_file.namelist()
        assert 'December_2024_Three_Month_Check-in_(Peer_Review)_Georgina_Johnson.pdf' in zip_file.namelist()

def test_hibob_to_pdf_no_file(client):
    response = client.post('/api/convert/hibob-to-pdf')
    assert response.status_code == 400
    assert response.json == {'error': 'No file provided'}

def test_hibob_to_pdf_invalid_file(client):
    file_data = BytesIO(b"not a json file")
    file_data.name = 'test.txt'
    response = client.post(
        '/api/convert/hibob-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.txt')}
    )
    assert response.status_code == 400
    assert response.json == {'error': 'Only JSON files are allowed'}

def test_hibob_to_pdf_invalid_json(client):
    file_data = BytesIO(b"{invalid json}")
    file_data.name = 'test.json'
    response = client.post(
        '/api/convert/hibob-to-pdf',
        content_type='multipart/form-data',
        data={'file': (file_data, 'test.json')}
    )
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid JSON file'}