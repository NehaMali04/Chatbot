import json
import string
import sys
import os
from http.server import BaseHTTPRequestHandler
from difflib import SequenceMatcher

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from faq_data_inline import FAQ_DATA

faq_data = [{"question": q.lower(), "answer": a} for q, a in FAQ_DATA]

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
        common_words = set(user_q.split()).intersection(set(faq_q.split()))
        if common_words:
            score += len(common_words) * 0.1
        if score > best_score:
            best_score = score
            best_match = faq
    return best_match, best_score

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            user_message = body.get("message", "")

            if not user_message:
                reply = "Please ask a question."
            else:
                best_match, score = find_best_match(user_message)
                reply = best_match["answer"] if best_match and score > 0.3 else "Sorry, I couldn't find a relevant answer."

            self._respond(200, {"response": reply})
        except Exception as e:
            self._respond(500, {"response": f"Error: {str(e)}"})

    def _respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)
