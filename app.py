import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # يحاول فتح الصفحة الرئيسية
        return render_template('index.html')
    except Exception as e:
        # إذا وجد خطأ في الملفات يظهره لك لتعرف أين المشكلة
        return f"خطأ في قوالب التصميم: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    # كود البحث الذي طورناه سابقاً
    return jsonify({"found": False}) # مؤقتاً للتجربة

if __name__ == '__main__':
    app.run(debug=True)
    
