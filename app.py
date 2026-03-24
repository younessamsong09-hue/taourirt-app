import os
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# دالة جلب البيانات من المجلد الوطني
def fetch_all_data():
    all_records = []
    # استخدام app.root_path ضروري لعمل المسارات على Vercel
    base_path = os.path.join(app.root_path, 'national')
    
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_records.extend(data)
                except:
                    continue
    return all_records

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('prompt', '').lower()
    
    # الكلمات المفتاحية لتفعيل المولد القانوني
    trigger_words = ['طلب', 'شكاية', 'تحرير', 'اكتب']
    if any(word in user_input for word in trigger_words):
        return jsonify({
            "found": True,
            "results": [{
                "type": "generator",
                "title": "محرر الوثائق القانونية",
                "docs": "جاهز لتحويل بياناتك إلى وثيقة PDF..."
            }]
        })

    all_data = fetch_all_data()
    matches = [
        item for item in all_data 
        if user_input in item.get('keywords', '').lower() or user_input in item.get('title', '').lower()
    ]
    
    if matches:
        return jsonify({"found": True, "results": matches[:5]})
    
    return jsonify({"found": False, "message": "لم نجد نتائج، حاول البحث عن: جواز سفر، بطاقة وطنية..."})

if __name__ == "__main__":
    app.run(debug=True)
    
