import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # يحاول فتح الفهرس، وإذا نجح سيظهر كل شيء
        return render_template('index.html')
    except Exception as e:
        # إذا فشل، سيخبرك بالملف الناقص (مثلاً: footer.html not found)
        return f"⚠️ عذراً يوسف، هناك خطأ في الربط بين الملفات: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    # كود البحث التجريبي ليتأكد أن المحرك يعمل
    data = request.get_json()
    query = data.get('prompt', '').lower()
    
    if "حفر" in query:
        return jsonify({
            "found": True,
            "title": "تعويض عن حفر الطرق 🕳️",
            "docs": "صور الحفرة، محضر الدرك/الشرطة، وفواتير الإصلاح.",
            "cost": "مجاني",
            "location": "المحكمة الإدارية أو شركة الطرق السيار"
        })
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
