import os
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import json
import torch
from spellchecker import SpellChecker  # Using pyspellchecker
import datetime
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Lazy-load the SBERT model
model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model

# Load the database of intents and responses
with open('database.json', 'r') as f:
    intents = json.load(f)

# Precompute encodings for intent patterns
intent_encodings = {
    intent['tag']: get_model().encode(intent['patterns'], convert_to_tensor=True)
    for intent in intents['intents']
}

# Initialize the spell checker
spell = SpellChecker()

def correct_spelling(user_input):
    words = user_input.split()
    corrected_words = [spell.correction(word) if word not in spell else word for word in words]
    return " ".join(corrected_words)

def predict_tag(sentence, threshold=0.5):
    sentence_embedding = get_model().encode(sentence, convert_to_tensor=True)
    
    max_similarity = -1
    predicted_tag = None

    for tag, encodings in intent_encodings.items():
        cosine_scores = util.pytorch_cos_sim(sentence_embedding, encodings)
        max_score = torch.max(cosine_scores).item()
        
        if max_score > max_similarity:
            max_similarity = max_score
            predicted_tag = tag

    if max_similarity < threshold:
        return "unknown"

    return predicted_tag

def get_response(predicted_tag):
    if predicted_tag == "unknown":
        return ["Sorry, I didn't understand that. Could you please rephrase?"]

    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return intent['responses']
    return ["Sorry, I don't understand that."]

# Optional in-memory logging
log_buffer = io.StringIO()

def log_chat(user_input, corrected_input, response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - User Input: {user_input} | Corrected Input: {corrected_input} | Response: {response}\n"
    log_buffer.write(log_entry)

@app.route('/')
def home():
    return "Chatbot is running."

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify(response="Please provide a valid input."), 400

        corrected_input = correct_spelling(user_input)
        predicted_tag = predict_tag(corrected_input)
        response = get_response(predicted_tag)

        log_chat(user_input, corrected_input, response[0])

        return jsonify(response=response[0], corrected_input=corrected_input)
    except Exception as e:
        return jsonify(response="An error occurred: {}".format(str(e))), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's expected port
    app.run(host="0.0.0.0", port=port, debug=False, threaded=False)
