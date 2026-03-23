import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_data():
    # هذا المسار يقرأ من مجلد national وملف emergency_solutions.json
    path = os.path.join('national', 'emergency_solutions.json')
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f).get('solutions', [])
    except:
        return []
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '').lower().strip()
    
    solutions = get_data()
    
    # محرك بحث ذكي يقطع كلمات المستخدم ويبحث عنها
    user_words = query.split()
    for item in solutions:
        search_pool = " ".join(item.get('keywords', [])) + " " + item.get('title', '').lower()
        if any(word in search_pool for word in user_words):
            return jsonify({"found": True, **item})
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
