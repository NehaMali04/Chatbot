import json
import string
import os
from http.server import BaseHTTPRequestHandler
from difflib import SequenceMatcher

# Load FAQ data from faq.json
faq_data = []

faq_path = os.path.join(os.path.dirname(__file__), '..', 'faq.json')
with open(faq_path, 'r', encoding='utf-8') as f:
    raw = json.load(f)
    for item in raw:
        faq_data.append({
            "question": item["question"].lower(),
            "answer": item["answer"]
        })

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def find_best_match(user_question):
    user_q = preprocess(user_question)
    best_match = None
    best_score = 0

    for faq in faq_data:
        faq_q = preprocess(faq["question"])
        score = SequenceMatcher(None, user_q, faq_q).ratio()
        user_words = set(user_q.split())
        faq_words = set(faq_q.split())
        common_words = user_words.intersection(faq_words)
        if common_words:
            score += len(common_words) * 0.1
        if score > best_score:
            best_score = score
            best_match = faq

    return best_match, best_score

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)
        user_message = data.get("message", "")

        if not user_message:
            reply = "Please ask a question."
        else:
            best_match, score = find_best_match(user_message)
            if best_match and score > 0.3:
                reply = best_match["answer"]
            else:
                reply = "Sorry, I couldn't find a relevant answer. Please try rephrasing your question."

        response = json.dumps({"response": reply})
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
