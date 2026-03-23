import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# وظيفة البحث عن البيانات داخل المجلد الوطني الجديد
def load_all_data():
    mega_database = {}
    # قمنا بتغيير المسار إلى 'national' ليتوافق مع مستودعك الحالي
    base_path = 'national' 
    
    if not os.path.exists(base_path):
        return mega_database

    # الكود سيمر الآن داخل كل ملفات الـ JSON في مجلد national
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        mega_database.update(file_data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    continue
    return mega_database

# واجهة المستخدم (HTML) مع الهوية الوطنية الجديدة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>المنصة الوطنية للتوجيه الإداري 🇲🇦</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Tajawal', sans-serif; background-color: #f4f4f4; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 5px solid #c1272d; }
        h1 { color: #006233; margin-bottom: 10px; }
        p { color: #666; }
        input { width: 90%; padding: 12px; margin: 15px 0; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; outline: none; transition: 0.3s; }
        input:focus { border-color: #006233; }
        button { background-color: #006233; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
        #result { margin-top: 20px; text-align: right; display: none; padding: 15px; background: #f9f9f9; border-radius: 8px; border-right: 5px solid #006233; }
        .info-item { margin-bottom: 10px; line-height: 1.6; }
        .label { font-weight: bold; color: #c1272d; }
        .official-btn { display: inline-block; margin-top: 10px; background: #c1272d; color: white; text-decoration: none; padding: 8px 15px; border-radius: 5px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>المنصة الوطنية 🇲🇦</h1>
        <p>دليلك الشامل للمساطر الإدارية في المغرب</p>
        <input type="text" id="userQuery" placeholder="مثلاً: باسبور، دعم، بيرمي...">
        <br>
        <button onclick="askBot()">بحث الآن</button>
        <div id="result"></div>
    </div>

    <script>
        async function askBot() {
            const query = document.getElementById('userQuery').value;
            const resultDiv = document.getElementById('result');
            
            if (!query) return;

            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'جاري البحث...';

            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: query })
            });

            const data = await response.json();
            if (data.found) {
                resultDiv.innerHTML = `
                    <h3>${data.title}</h3>
                    <div class="info-item"><span class="label">📄 الوثائق المطلوبة:</span> ${data.docs}</div>
                    <div class="info-item"><span class="label">💰 التكلفة:</span> ${data.cost}</div>
                    <div class="info-item"><span class="label">⏳ الوقت المتوقع:</span> ${data.time}</div>
                    <div class="info-item"><span class="label">📍 المكان:</span> ${data.location}</div>
                    <a href="${data.link}" class="official-btn" target="_blank">الموقع الرسمي للمسطرة</a>
                `;
            } else {
                resultDiv.innerHTML = '<p style="color:red;">عذراً، لم أجد معلومات حول هذا الموضوع حالياً. جرب كلمات أخرى.</p>';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('prompt', '').lower()
    all_services = load_all_data()
    
    for service_id, info in all_services.items():
        if any(word in user_query for word in info['keywords']):
            return jsonify({
                "found": True,
                "title": info['title'],
                "docs": info['docs'],
                "cost": info['cost'],
                "time": info['time'],
                "location": info['location'],
                "link": info.get('link', '#')
            })
            
    return jsonify({"found": False})

if __name__ == "__main__":
    app.run(debug=True)
                           
