import os
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# قاعدة بيانات مؤقتة لخدمة "صوت المجتمع"
community_reports = [
    {"text": "مرحباً بكم في منصة وثيقتي - تاوريرت الحية", "time": "الآن"}
]

# دالة ذكية لجلب البيانات من مجلد national لضمان التوافق مع Vercel
def fetch_all_data():
    all_records = []
    # استخدام app.root_path لضمان الوصول للمجلد في السيرفر
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
    return render_template('index.html', reports=community_reports)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('prompt', '').lower()
    
    # محرك التوجيه الذكي للمولدات (مثل الطلبات الخطية)
    trigger_words = ['طلب', 'شكاية', 'تحرير', 'اكتب']
    if any(word in user_input for word in trigger_words):
        return jsonify({
            "found": True,
            "results": [{
                "type": "generator",
                "title": "محرر الوثائق القانونية الفوري",
                "docs": "النظام جاهز لتحرير طلبك. يرجى ملء البيانات أدناه."
            }]
        })

    # محرك البحث في البيانات الوطنية
    all_data = fetch_all_data()
    matches = [
        item for item in all_data 
        if user_input in item.get('keywords', '').lower() or user_input in item.get('title', '').lower()
    ]
    
    if matches:
        return jsonify({"found": True, "results": matches[:5]})
    
    return jsonify({"found": False, "message": "لم نجد نتائج دقيقة، جرب كلمات مثل: جواز سفر، بطاقة وطنية..."})

@app.route('/report', methods=['POST'])
def handle_report():
    msg = request.json.get('text')
    if msg:
        new_entry = {"text": msg, "time": datetime.now().strftime("%H:%M")}
        community_reports.insert(0, new_entry)
        return jsonify({"status": "success", "all_reports": community_reports[:10]})
    return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(debug=True)
    
