import os
import json
import re
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# تحديد المسار الديناميكي لمجلد البيانات لضمان عمله على Vercel
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def clean_text(text):
    """تنظيف النص من الحركات والمسافات الزائدة لتوحيد البحث"""
    if not text: return ""
    text = text.lower().strip()
    # إزالة ال التعريف لزيادة دقة البحث (اختياري)
    text = re.sub(r'^(ال)', '', text)
    return text

def load_all_data():
    """قراءة ومج جميع ملفات JSON في قاعدة بيانات واحدة مؤقتة"""
    mega_database = {}
    if not os.path.exists(BASE_PATH):
        return mega_database
    
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        mega_database.update(json.load(f))
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    return mega_database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = clean_text(data.get('prompt', ''))
    
    if not user_query:
        return jsonify({"found": False})

    database = load_all_data()
    search_tokens = user_query.split() # تقسيم جملة المستخدم لعدة كلمات

    best_match = None
    max_score = 0

    for key, value in database.items():
        # إنشاء "وعاء نصي" يحتوي على كل المعلومات لزيادة فرص العثور على الكلمة
        search_pool = clean_text(
            value.get('title', '') + " " + 
            " ".join(value.get('keywords', [])) + " " +
            key
        )

        # حساب عدد الكلمات المشتركة بين بحث المستخدم وقاعدة البيانات
        score = sum(1 for token in search_tokens if token in search_pool)

        if score > max_score:
            max_score = score
            best_match = value

    if best_match and max_score > 0:
        return jsonify({
            "found": True,
            "title": best_match.get('title'),
            "docs": best_match.get('docs'),
            "cost": best_match.get('cost'),
            "time": best_match.get('time'),
            "location": best_match.get('location'),
            "link": best_match.get('link')
        })
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
