import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# تحديد المسار لمجلد national الذي يحتوي على ملفاتك الـ 25
BASE_PATH = os.path.join(os.path.dirname(__file__), 'national')

def load_mega_database():
    """وظيفة لجمع كل الحلول من كافة ملفات JSON"""
    all_solutions = []
    if not os.path.exists(BASE_PATH):
        return all_solutions
    
    for file in os.listdir(BASE_PATH):
        if file.endswith('.json'):
            try:
                with open(os.path.join(BASE_PATH, file), 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    # دعم نظام القوائم (solutions) الموجود في ملفاتك الجديدة
                    if 'solutions' in file_data:
                        all_solutions.extend(file_data['solutions'])
                    # دعم النظام القديم إذا وجد
                    else:
                        for val in file_data.values():
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

    database = load_mega_database()
    user_words = query.split()
    
    for item in database:
        # البحث في العنوان والكلمات المفتاحية
        search_pool = (item.get('title', '') + " " + " ".join(item.get('keywords', []))).lower()
        
        if any(word in search_pool for word in user_words):
            return jsonify({
                "found": True,
                "title": item.get('title'),
                "docs": item.get('docs'),
                "cost": item.get('cost'),
                "time": item.get('time', 'غير محدد'),
                "location": item.get('location'),
                "link": item.get('link', '') # هنا يتم استحضار الرابط الإلكتروني
            })
            
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
