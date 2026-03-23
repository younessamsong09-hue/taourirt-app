import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_logic(user_query):
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    try:
        # هنا التعديل: السيرفر سيبحث الآن داخل مجلد national
        json_path = os.path.join('national', 'solutions.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for item in data['solutions']:
                # البحث في الكلمات المفتاحية والعنوان معاً
                search_content = " ".join(item['keywords']) + " " + item['title'].lower()
                
                # التحقق إذا كانت أي كلمة من بحث المستخدم موجودة
                user_words = user_query.split()
                if any(word in search_content for word in user_words):
                    return item
    except Exception as e:
        print(f"Error: {e}")
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '')
    result = search_logic(query)
    
    if result:
        return jsonify({"found": True, **result})
    return jsonify({"found": False})
    
