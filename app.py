import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# وظيفة ذكية لجلب البيانات من مجلد national
def load_all_data():
    mega_database = {}
    base_path = 'national' 
    if not os.path.exists(base_path):
        return mega_database

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    mega_database.update(json.load(f))
    return mega_database

@app.route('/')
def index():
    # سيقوم Flask الآن بفتح ملف templates/index.html الذي أنشأته
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '').lower()
    db = load_all_data()
    
    for key, val in db.items():
        if query in key.lower() or any(k in query for k in val.get('keywords', [])):
            return jsonify({"found": True, **val})
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
