from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
from summarizer import summarize_article
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/process_link', methods=['POST'])
def process_link():
    data = request.json
    link = data.get('link', 'No link provided')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Link hovered: {link}")
    summary = summarize_article(link)
    
    return jsonify({
        "data": summary
    })

if __name__ == '__main__':
    print("Starting HoverZoom link processing server on http://localhost:5000")
    print("Hovered links will be logged to hovered_links.log")
    app.run(host='127.0.0.1', port=5000, debug=True)
