import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دالة ذكية لقراءة جميع القطاعات الوطنية من مجلد national
def get_national_data():
    all_data = []
    # تحديد مسار المجلد (يعمل على الكمبيوتر وعلى Vercel)
    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_path, 'national')
    
    if not os.path.exists(folder_path):
        return all_data

    # قراءة كل ملف JSON على حدة (ملف للهوية، ملف للحقوق، ملف للمال...)
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    # دمج البيانات مع الحفاظ على مصدرها (اسم الملف يعبر عن القسم)
                    category_name = filename.replace('.json', '')
                    if isinstance(content, list):
                        for item in content:
                            item['category'] = category_name
                            all_data.append(item)
                    else:
                        content['category'] = category_name
                        all_data.append(content)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return all_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('prompt', '').lower()
    data_source = get_national_data()
    results = []

    # محرك بحث ذكي يبحث في العناوين والكلمات المفتاحية والمحتوى
    for item in data_source:
        search_space = f"{item.get('title', '')} {item.get('keywords', '')} {item.get('docs', '')}".lower()
        if user_query in search_space:
            results.append(item)

    if results:
        # إرجاع النتيجة الأكثر صلة (أو قائمة نتائج)
        return jsonify({
            "found": True, 
            "results": results[:3] # إرجاع أفضل 3 نتائج
        })
    
    return jsonify({"found": False, "message": "لم نجد نتيجة دقيقة، حاول تغيير كلمات البحث."})

if __name__ == '__main__':
    app.run(debug=True)
    
