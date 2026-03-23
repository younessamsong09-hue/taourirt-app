import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# تحديد المسار لمجلد national
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def load_mega_data():
    """هذه الوظيفة تجمع الـ 25 ملفاً في قاعدة بيانات واحدة ضخمة"""
    all_solutions = []
    if not os.path.exists(BASE_PATH):
        return all_solutions
    
    # الدوران على كل الملفات الـ 25
    for file in os.listdir(BASE_PATH):
        if file.endswith('.json'):
            try:
                with open(os.path.join(BASE_PATH, file), 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    
                    # إذا كان الملف يحتوي على قائمة solutions (النظام الجديد)
                    if 'solutions' in file_data:
                        all_solutions.extend(file_data['solutions'])
                    
                    # إذا كان الملف بنظام القاموس (النظام القديم)
                    else:
                        for key, val in file_data.items():
                            if isinstance(val, dict):
                                all_solutions.append(val)
            except Exception as e:
                print(f"Error loading {file}: {e}")
                
    return all_solutions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '').strip().lower()
    
    if not query:
        return jsonify({"found": False})

    # تحميل كل البيانات من الـ 25 ملفاً
    database = load_mega_data()
    
    # البحث بذكاء: كلمة واحدة من المستخدم تكفي
    user_words = query.split()
    
    for item in database:
        title = str(item.get('title', '')).lower()
        # تحويل الكلمات المفتاحية لنص واحد للبحث فيه
        keywords_list = item.get('keywords', [])
        keywords_text = " ".join(keywords_list).lower()
        
        search_pool = title + " " + keywords_text
        
        # إذا وجدنا أي كلمة من بحث المستخدم داخل هذا الحل
        if any(word in search_pool for word in user_words):
            return jsonify({
                "found": True,
                "title": item.get('title'),
                "docs": item.get('docs'),
                "cost": item.get('cost'),
                "time": item.get('time', 'غير محدد'),
                "location": item.get('location'),
                "link": item.get('link', '#')
            })
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
