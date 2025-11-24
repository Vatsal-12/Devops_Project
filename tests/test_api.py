# tests/test_api.py
import json
import pytest
from app.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data

def test_predict_success(client):
    payload = {"text": "I love this product, it is awesome"}
    resp = client.post("/predict", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["prediction"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert "confidence" in data
    assert data["original_text"] == payload["text"]

def test_predict_bad_request(client):
    resp = client.post("/predict", data=json.dumps({}), content_type="application/json")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
