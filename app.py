import os
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# قاعدة بيانات حية مؤقتة لـ "صوت المجتمع" (الجمع والنقاش)
community_reports = [
    {"text": "مرحباً بكم في منصة وطني - تاوريرت الحية", "time": "الآن"}
]

# دالة ذكية لجلب البيانات من أي ملف JSON في مجلد national
def fetch_all_data():
    all_records = []
    base_path = os.path.join(app.root_path, 'national')
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.endswith('.json'):
                with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_records.extend(data)
                    except: continue
    return all_records

@app.route('/')
def index():
    return render_template('index.html', reports=community_reports)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('prompt', '').lower()
    
    # 1. نظام التحرير الفوري (المحرر الذكي)
    trigger_words = ['شكاية', 'اكتب', 'تحرير', 'تظلم', 'طلب']
    if any(word in user_input for word in trigger_words):
        return jsonify({
            "found": True,
            "results": [{
                "type": "generator",
                "title": "محرر الوثائق القانونية الفوري",
                "docs": "النظام جاهز لتحرير وثيقتك الرسمية. يرجى ملء البيانات أدناه لتحويلها إلى PDF جاهز للطباعة."
            }]
        })

    # 2. نظام البحث والتحليل (قاموس الدارجة + البيانات الضخمة)
    dialect = {"لاكارط": "بطاقة", "برمي": "رخصة", "باسبور": "جواز", "قهوة": "رشوة"}
    for k, v in dialect.items():
        if k in user_input: user_input += f" {v}"

    all_data = fetch_all_data()
    # بحث ذكي يعتمد على العنوان أو الكلمات الدالة
    matches = [
        item for item in all_data 
        if user_input in item.get('keywords', '').lower() or user_input in item.get('title', '').lower()
    ]

    if matches:
        return jsonify({"found": True, "results": matches[:5]})
    
    return jsonify({"found": False, "message": "لم نجد نتائج دقيقة، جرب كلمات مثل: الأسعار، ضياع، أو دعم."})

@app.route('/report', methods=['POST'])
def handle_report():
    msg = request.json.get('text')
    if msg:
        new_entry = {"text": msg, "time": datetime.now().strftime("%H:%M")}
        community_reports.insert(0, new_entry) # يظهر الأحدث أولاً
        return jsonify({"status": "success", "all_reports": community_reports[:10]})
    return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)
    
