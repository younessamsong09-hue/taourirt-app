import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# وظيفة البحث عن البيانات داخل المجلد الوطني
def load_all_data():
    mega_database = {}
    base_path = 'national' 
    
    if not os.path.exists(base_path):
        return mega_database

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        mega_database.update(file_data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    continue
    return mega_database

@app.route('/')
def index():
    # الآن سيقوم Flask بالبحث عن index.html داخل مجلد templates تلقائياً
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('prompt', '').lower()
    
    database = load_all_data()
    
    # منطق بحث بسيط ومطور
    for key, value in database.items():
        # البحث في العنوان أو الكلمات المفتاحية
        if user_query in key.lower() or any(kw in user_query for kw in value.get('keywords', [])):
            return jsonify({
                "found": True,
                "title": value.get('title'),
                "docs": value.get('docs'),
                "cost": value.get('cost'),
                "time": value.get('time'),
                "location": value.get('location'),
                "link": value.get('link')
            })
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
