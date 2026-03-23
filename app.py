import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_in_json(query):
    try:
        with open('data/solutions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data['solutions']:
                if any(key in query for key in item['keywords']):
                    return item
    except:
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.get_json()
    query = user_data.get('prompt', '').lower()
    result = search_in_json(query)
    
    if result:
        return jsonify({"found": True, **result})
    return jsonify({"found": False})
    
