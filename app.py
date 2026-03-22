from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# قاعدة بيانات ذكية محلية - تعمل 24/7 بدون أعطال
TAOURIRT_KNOWLEDGE = {
    "البطاقة الوطنية": "📌 **للحصول على CIN في تاوريرت:** <br>1. شهادة السكنى من الأمن الوطني.<br>2. 4 صور فوتوغرافية حديثة.<br>3. نسخة من عقد الازدياد.<br>4. واجبات التمبر (75 درهم).<br>📍 توجه لمفوضية الشرطة المركزية.",
    "جواز السفر": "✈️ **استخراج الباسبور:**<br>1. شراء التمبر الإلكتروني (300-500 درهم).<br>2. بطاقة التعريف الوطنية صالحة.<br>3. صورتان فوتوغرافيتان.<br>📍 الطلب يتم عبر بوابة passport.ma ثم التوجه للملحقة الإدارية.",
    "عقد الازدياد": "👶 **الحصول على عقد الازدياد:**<br>يجب التوجه لمكتب الحالة المدنية بمكان الولادة (بلدية تاوريرت). أحضر معك الدفتر العائلي.",
    "رخصة السياقة": "🚗 **رخصة السياقة (البيرمي):**<br>يتطلب الفحص الطبي أولاً، ثم التسجيل في إحدى مدارس تعليم السياقة بتاوريرت، وتقديم ملف يشمل صوراً ونسخة من CIN.",
    "مرحبا": "أهلاً بك يا ابن تاوريرت! أنا مساعدك الذكي، اسألني عن أي وثيقة إدارية."
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة تاوريرت الرقمية</title>
    <style>
        :root { --primary: #1a5f7a; --secondary: #c0392b; --bg: #f8f9fa; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .app-container { width: 100%; max-width: 450px; height: 90vh; background: white; box-shadow: 0 20px 50px rgba(0,0,0,0.15); border-radius: 25px; display: flex; flex-direction: column; overflow: hidden; border: 2px solid #eee; }
        .header { background: var(--primary); color: white; padding: 25px; text-align: center; position: relative; }
        .header h2 { margin: 0; font-size: 22px; }
        .header p { margin: 5px 0 0; font-size: 13px; opacity: 0.8; }
        .chat-area { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; background: #ffffff; }
        .msg { padding: 12px 18px; border-radius: 20px; font-size: 15px; line-height: 1.6; max-width: 85%; position: relative; animation: fadeIn 0.3s ease; }
        .bot { background: #f0f2f5; color: #333; align-self: flex-start; border-bottom-right-radius: 5px; }
        .user { background: var(--primary); color: white; align-self: flex-end; border-bottom-left-radius: 5px; }
        .input-bar { padding: 15px; background: white; display: flex; gap: 10px; border-top: 1px solid #eee; }
        input { flex: 1; padding: 12px 20px; border-radius: 30px; border: 1px solid #ddd; outline: none; font-size: 15px; }
        button { background: var(--secondary); color: white; border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }
        button:hover { transform: scale(1.1); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h2>دليل تاوريرت الذكي 🇲🇦</h2>
            <p>معك يوسف ومساعده الذكي لخدمة المدينة</p>
        </div>
        <div id="chatBox" class="chat-area">
            <div class="msg bot">مرحباً بك! أنا رفيقك الذكي في تاوريرت. جرب أن تسألني عن (البطاقة الوطنية، جواز السفر، أو رخصة السياقة).</div>
        </div>
        <div class="input-bar">
            <input type="text" id="userInput" placeholder="اكتب سؤالك هنا...">
            <button onclick="ask()">➔</button>
        </div>
    </div>

    <script>
        function ask() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const val = input.value.trim();
            if(!val) return;

            chatBox.innerHTML += `<div class="msg user">${val}</div>`;
            input.value = '';
            
            fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            })
            .then(res => res.json())
            .then(data => {
                chatBox.innerHTML += `<div class="msg bot">${data.answer}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt', '')
    answer = "عذراً، لم أفهم سؤالك جيداً. جرب السؤال عن (البطاقة الوطنية) أو (جواز السفر)."
    
    for key in TAOURIRT_KNOWLEDGE:
        if key in prompt:
            answer = TAOURIRT_KNOWLEDGE[key]
            break
            
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run()
    
