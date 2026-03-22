import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# إعداد المفتاح
genai.configure(api_key="AIzaSyBUCXLU5GXhB86V5e8oH5RwWuwWJsmtoog")

# استخدام الموديل المستقر لتجنب خطأ 404
model = genai.GenerativeModel('gemini-pro')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مساعد تاوريرت</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; margin: 0; }
        .chat-card { background: white; width: 100%; max-width: 400px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 85vh; }
        .header { background: #1a5f7a; color: white; padding: 15px; text-align: center; }
        .chat-box { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .input-area { padding: 10px; display: flex; gap: 5px; border-top: 1px solid #eee; background: white; }
        input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid #ddd; outline: none; }
        button { background: #1a5f7a; color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; }
        .msg { padding: 10px; border-radius: 12px; font-size: 14px; max-width: 85%; line-height: 1.4; }
        .bot { background: #e8f4fd; align-self: flex-start; }
        .user { background: #1a5f7a; color: white; align-self: flex-end; }
    </style>
</head>
<body>
    <div class="chat-card">
        <div class="header"><h3>مساعد تاوريرت الذكي 🇲🇦</h3></div>
        <div id="chatBox" class="chat-box">
            <div class="msg bot">تم تحديث النظام لموديل Pro المستقر. كيف يمكنني مساعدتك الآن؟</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="اسألني أي شيء عن الوثائق...">
            <button onclick="askBot()">إرسال</button>
        </div>
    </div>
    <script>
        async function askBot() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            if (!input.value.trim()) return;
            const text = input.value;
            chatBox.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="msg bot">${data.answer}</div>`;
            } catch (e) {
                chatBox.innerHTML += `<div class="msg bot">حدث خطأ في الاتصال. حاول مرة أخرى.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
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
    try:
        user_prompt = request.json.get('prompt')
        # استخدام موديل Pro وحذف v1beta من الإعدادات لضمان التوافق
        response = model.generate_content("أجب كمساعد إداري مغربي يساعد سكان مدينة تاوريرت: " + user_prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({'answer': "عذراً، ما زال هناك مشكل في مفتاح API أو الموديل: " + str(e)})

if __name__ == "__main__":
    app.run()
    
