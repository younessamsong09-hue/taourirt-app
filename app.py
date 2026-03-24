import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دالة جلب البيانات من المجلد الوطني
def get_national_data():
    all_data = []
    # استخدام المسار المطلق لضمان عمله على Vercel
    base_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_path, "national")

    if not os.path.exists(folder_path):
        return all_data

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                    content = json.load(f)
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
    
    # الكلمات المفتاحية لتفعيل محرر الطلبات (المولد)
    trigger_words = ['طلب', 'شكاية', 'تحرير', 'كتابة']
    if any(word in user_query for word in trigger_words):
        return jsonify({
            "found": True,
            "results": [{
                "type": "generator",
                "title": "محرر الوثائق القانونية",
                "docs": "النظام جاهز لتحويل بياناتك إلى وثيقة PDF رسمية."
            }]
        })

    data_source = get_national_data()
    results = []
    
    for item in data_source:
        search_space = f"{item.get('title', '')} {item.get('keywords', '')} {item.get('docs', '')}".lower()
        if user_query in search_space:
            results.append(item)
            
    if results:
        return jsonify({"found": True, "results": results[:5]})
    
    return jsonify({"found": False, "message": "لم يتم العثور على نتائج دقيقة، حاول تغيير كلمات البحث."})

if __name__ == "__main__":
    app.run(debug=True)
    
