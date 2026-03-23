import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_in_all_files(user_query):
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    national_dir = 'national'
    if not os.path.exists(national_dir): return None

    # البحث في كل ملفات الـ JSON داخل مجلد national
    for filename in os.listdir(national_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(national_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    solutions = data.get('solutions', [])
                    
                    for item in solutions:
                        # دمج الكلمات المفتاحية والعنوان للبحث
                        search_pool = " ".join(item.get('keywords', [])) + " " + item.get('title', '').lower()
                        
                        # إذا وجدنا الكلمة في أي ملف
                        user_words = user_query.split()
                        if any(word in search_pool for word in user_words):
                            return item
            except:
                continue
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '')
    result = search_in_all_files(query)
    
    if result:
        return jsonify({"found": True, **result})
    return jsonify({"found": False})
    
