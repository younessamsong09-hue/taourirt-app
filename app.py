import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_logic(user_query):
    # تحويل النص لمدار صغير وحذف الفراغات
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    try:
        # الربط مع مجلد national وملف emergency_solutions.json
        json_path = os.path.join('national', 'emergency_solutions.json')
        
        if not os.path.exists(json_path):
            return None

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            solutions = data.get('solutions', [])
            
            # تقطيع بحث المستخدم لكلمات (مثلاً: "تعويض الضو" تصبح "تعويض" و "الضو")
            user_words = user_query.split()
            
            for item in solutions:
                # جمع الكلمات المفتاحية والعنوان في نص واحد للبحث فيه
                keywords_list = item.get('keywords', [])
                title = item.get('title', '').lower()
                search_content = " ".join(keywords_list) + " " + title
                
                # إذا وجدت أي كلمة من كلمات المستخدم داخل محتوى الحل
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
        return jsonify({
            "found": True, 
            "title": result.get('title'),
            "docs": result.get('docs'),
            "cost": result.get('cost'),
            "location": result.get('location')
        })
    return jsonify({"found": False})
    
