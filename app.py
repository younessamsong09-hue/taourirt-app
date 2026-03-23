import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# المسار الرئيسي لقاعدة البيانات
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def get_all_solutions():
    """وظيفة ذكية تقرأ أي عدد من الملفات في أي مجلد فرعي داخل national"""
    all_data = []
    if not os.path.exists(BASE_PATH):
        return all_data

    # os.walk تسمح لنا بالدخول للمجلدات الفرعية أيضاً مستقبلاً
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        # استخراج البيانات سواء كانت قائمة أو قاموس
                        if isinstance(content, dict) and 'solutions' in content:
                            all_data.extend(content['solutions'])
                        elif isinstance(content, list):
                            all_data.extend(content)
                        elif isinstance(content, dict):
                            # إذا كان الملف عبارة عن قاموس مباشر (النظام القديم)
                            for key, value in content.items():
                                if isinstance(value, dict):
                                    all_data.append(value)
                except Exception as e:
                    print(f"⚠️ خطأ في قراءة الملف {file}: {e}")
    return all_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('prompt', '').strip().lower()
    
    if not user_query:
        return jsonify({"found": False})

    # جلب كل البيانات من الـ 25 ملفاً (أو أكثر)
    all_solutions = get_all_solutions()
    search_words = user_query.split()

    for item in all_solutions:
        # البحث في العنوان، الكلمات المفتاحية، وحتى مكان الإيداع لزيادة دقة النتائج
        title = str(item.get('title', '')).lower()
        keywords = " ".join(item.get('keywords', [])).lower()
        location = str(item.get('location', '')).lower()
        
        search_pool = f"{title} {keywords} {location}"
        
        if any(word in search_pool for word in search_words):
            return jsonify({
                "found": True,
                "title": item.get('title'),
                "docs": item.get('docs'),
                "cost": item.get('cost'),
                "location": item.get('location'),
                "time": item.get('time', 'غير محدد'),
                "link": item.get('link', '') # سيبقى جاهزاً لليوم الذي تقرر فيه تفعيله
            })

    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
