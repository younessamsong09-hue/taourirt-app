import os
import json
import re
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# تحديد مسار مجلد البيانات لضمان قراءته بشكل صحيح على Vercel
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def clean_text(text):
    """تنظيف النص لتوحيد عملية البحث وتجاهل الأخطاء البسيطة"""
    if not text: return ""
    text = text.lower().strip()
    # إزالة ال التعريف لجعل البحث أكثر مرونة (مثلاً: "جواز" تجد "الجواز")
    text = re.sub(r'^(ال)', '', text)
    return text

def load_all_data():
    """قراءة كافة ملفات JSON من مجلد national ودمجها"""
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
    # تقسيم بحث المستخدم لكلمات مفردة للبحث عنها
    user_tokens = user_query.split()

    best_match = None
    highest_score = 0

    for key, value in database.items():
        # إنشاء نص شامل للبحث داخل كل خدمة (العنوان + الكلمات المفتاحية + الكود)
        search_pool = clean_text(
            str(value.get('title', '')) + " " + 
            " ".join(value.get('keywords', [])) + " " + 
            str(key)
        )

        # حساب عدد الكلمات التي تطابقت من بحث المستخدم مع قاعدة البيانات
        match_score = sum(1 for token in user_tokens if token in search_pool)

        # إذا وجدنا تطابقاً أفضل، نحفظ النتيجة
        if match_score > highest_score:
            highest_score = match_score
            best_match = value

    # إذا وجدنا نتيجة (على الأقل كلمة واحدة مطابقة)
    if best_match and highest_score > 0:
        return jsonify({
            "found": True,
            "title": best_match.get('title'),
            "docs": best_match.get('docs'),
            "cost": best_match.get('cost'),
            "time": best_match.get('time'),
            "location": best_match.get('location'),
            "link": best_match.get('link', '#')
        })
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
