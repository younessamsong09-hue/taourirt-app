import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# تحديد مسار المجلد الذي يحتوي على ملفات JSON (national)
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def load_all_data():
    """وظيفة لجمع كافة البيانات من ملفات JSON في مجلد national"""
    mega_database = {}
    if not os.path.exists(BASE_PATH):
        return mega_database
    
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        mega_database.update(file_data)
                except Exception as e:
                    print(f"خطأ في تحميل الملف {file}: {e}")
    return mega_database

@app.route('/')
def index():
    # سيقوم Flask الآن بالبحث تلقائياً عن templates/index.html
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('prompt', '').strip().lower()
    
    if not user_query:
        return jsonify({"found": False})

    database = load_all_data()
    
    # البحث في العناوين والكلمات المفتاحية
    for key, value in database.items():
        title = value.get('title', '').lower()
        keywords = [k.lower() for k in value.get('keywords', [])]
        
        if user_query in title or user_query in key.lower() or any(user_query in kw for kw in keywords):
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
    
