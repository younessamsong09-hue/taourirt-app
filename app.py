import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# دالة للتأكد من وجود الملفات قبل محاولة فتحها
def check_template(name):
    path = os.path.join('templates', name)
    return os.path.exists(path)

@app.route('/')
def index():
    # التأكد من وجود الملفات الأساسية لتجنب "Internal Server Error"
    required_files = ['base.html', 'index.html', 'ticker.html', 'footer.html']
    missing = [f for f in required_files if not check_template(f)]
    
    if missing:
        return f"⚠️ عذراً يوسف، هناك ملفات مفقودة في مجلد templates: {', '.join(missing)}"
    
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # كود البحث الصوتي والذكي الذي طورناه
    data = request.get_json()
    query = data.get('prompt', '').lower()
    
    # مثال بسيط للرد (سنطوره ليربط بملفات الـ JSON لاحقاً)
    if "حفر" in query or "طريق" in query:
        return jsonify({
            "found": True,
            "title": "تعويض عن حفر الطرق 🕳️",
            "docs": "محضر معاينة، صور الحفرة، فواتير الإصلاح، وشهادة التأمين.",
            "cost": "مجاني (مطالبة قضائية أو ودية)",
            "location": "الجماعة المحلية أو شركة الطرق السيار"
        })
    
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
