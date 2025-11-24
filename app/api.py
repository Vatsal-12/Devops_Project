# app/api.py
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from app.preprocess import clean_text, tokenize
from app.model import LexiconSentiment

app = Flask(__name__)
model = LexiconSentiment()

class InputPayload(BaseModel):
    text: str

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Sentiment API (Flask) running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = InputPayload(**request.get_json(force=True))
    except (ValidationError, TypeError):
        return jsonify({"error": "Invalid payload. Provide JSON with field 'text'."}), 400

    cleaned = clean_text(payload.text)
    tokens = tokenize(cleaned)
    result = model.predict(tokens)

    response = {
        "original_text": payload.text,
        "cleaned_text": cleaned,
        "prediction": result["label"],
        "confidence": result["score"],
        "pos_count": result["pos_count"],
        "neg_count": result["neg_count"],
        "tokens_total": result["tokens_total"]
    }
    return jsonify(response), 200
