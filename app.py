from flask import Flask, request, jsonify
from textblob import TextBlob
import json
import datetime
from flask_cors import CORS
import difflib

app = Flask(__name__)
CORS(app)

# Load the database of intents and responses
with open('database.json', 'r') as f:
    intents = json.load(f)

# Prepare a dictionary to map each pattern to its intent tag
pattern_to_intent = {}
for intent in intents['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        pattern_to_intent[pattern] = tag

# Convert patterns to a list for use with difflib
all_patterns = list(pattern_to_intent.keys())

def correct_spelling(user_input):
    blob = TextBlob(user_input)
    corrected_text = str(blob.correct())
    return corrected_text

def predict_tag(sentence, threshold=0.5):
    closest_matches = difflib.get_close_matches(sentence, all_patterns, n=1, cutoff=threshold)
    
    if closest_matches:
        best_match = closest_matches[0]
        return pattern_to_intent.get(best_match, "unknown")
    else:
        return "unknown"

def get_response(predicted_tag):
    if predicted_tag == "unknown":
        return ["Sorry, I didn't understand that. Could you please rephrase?"]

    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return intent['responses']
    return ["Sorry, I don't understand that."]

def log_chat(user_input, corrected_input, response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - User Input: {user_input} | Corrected Input: {corrected_input} | Response: {response}\n"
    
    with open('chat_log.txt', 'a') as log_file:
        log_file.write(log_entry)

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
    app.run(host='0.0.0.0', port=10000, debug=False)

