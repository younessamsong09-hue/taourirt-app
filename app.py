import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# مخزن مؤقت لتبليغات المواطنين (الجمع والنقاش)
live_reports = []

def get_national_data():
    all_data = []
    base_dir = os.path.join(app.root_path, 'national')
    if os.path.exists(base_dir):
        for filename in os.listdir(base_dir):
            if filename.endswith('.json'):
                with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
                    all_data.extend(json.load(f))
    return all_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('prompt', '').lower()
    
    # 1. قاموس الدارجة المغربية
    dialect_map = {"لاكارط": "بطاقة", "برمي": "رخصة", "باسبور": "جواز", "قهوة": "رشوة", "تدويرة": "رشوة"}
    for k, v in dialect_map.items():
        if k in user_query: user_query += f" {v}"

    # 2. منطق التحرير الحي (إذا طلب المواطن كتابة شكاية)
    if any(word in user_query for word in ['اكتب', 'شكاية', 'تحرير']):
        return jsonify({"found": True, "results": [{
            "title": "محرر الشكايات الفوري",
            "type": "generator",
            "docs": "يمكنك الآن تحرير شكايتك الرسمية فوراً بلمسة واحدة.",
            "location": "منصة وطني - تاوريرت",
            "cost": "بالمجان"
        }]})

    # 3. البحث العادي في البيانات
    data_source = get_national_data()
    results = [item for item in data_source if user_query in str(item).lower()]
    
    if results:
        return jsonify({"found": True, "results": results[:3]})
    return jsonify({"found": False, "message": "لم نجد نتائج، جرب كلمات أخرى."})

# 4. استقبال تبليغات "صوت تاوريرت"
@app.route('/report', methods=['POST'])
def add_report():
    report = request.json.get('text')
    if report:
        live_reports.insert(0, report) # إضافة التبليغ في الأعلى
        return jsonify({"status": "success", "reports": live_reports[:5]})
    return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)
    
