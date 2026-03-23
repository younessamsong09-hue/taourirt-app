import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_logic(user_query):
    # تنظيف النص لضمان أفضل نتيجة بحث
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    try:
        # الربط المباشر مع ملفك في مجلد national
        json_path = os.path.join('national', 'emergency_solutions.json')
        
        if not os.path.exists(json_path):
            print(f"الملف غير موجود في المسار: {json_path}")
            return None

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # البحث داخل قائمة 'solutions'
            for item in data.get('solutions', []):
                # جمع الكلمات المفتاحية والعنوان للبحث الشامل
                search_pool = " ".join(item.get('keywords', [])) + " " + item.get('title', '').lower()
                
                # فحص كلمات المستخدم كلمة بكلمة
                user_words = user_query.split()
                if any(word in search_pool for word in user_words):
                    return item
    except Exception as e:
        print(f"خطأ في قراءة ملف JSON: {e}")
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
    
