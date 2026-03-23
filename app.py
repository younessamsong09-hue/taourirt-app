import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_in_json(query):
    query = query.lower().strip()
    try:
        # تأكد من أن مسار الملف صحيح كما أنشأته
        with open('data/solutions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            user_words = query.split() # تقطيع جملة المستخدم لكلمات
            
            for item in data['solutions']:
                # نجمع الكلمات المفتاحية والعنوان في نص واحد للبحث فيه
                content_to_search = " ".join(item['keywords']) + " " + item['title'].lower()
                
                # إذا وجدت أي كلمة من كلمات المستخدم داخل النص، أرجع النتيجة
                if any(word in content_to_search for word in user_words):
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
    user_data = request.get_json()
    query = user_data.get('prompt', '')
    result = search_in_json(query)
    
    if result:
        return jsonify({"found": True, **result})
    return jsonify({"found": False})
    
