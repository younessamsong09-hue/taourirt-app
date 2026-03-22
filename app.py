import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# إعداد الذكاء الاصطناعي بمفتاحك الخاص
genai.configure(api_key="AIzaSyBUCXLU5GXhB86V5e8oH5RwWuwWJsmtoog")

# استخدام اسم الموديل الأكثر استقراراً
model = genai.GenerativeModel('gemini-pro')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة تاوريرت الذكية</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .chat-card { background: white; width: 100%; max-width: 450px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .header { background: #1a5f7a; color: white; padding: 20px; text-align: center; }
        .chat-box { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; background: #fff; }
        .input-area { padding: 15px; border-top: 1px solid #eee; display: flex; gap: 8px; background: #f9f9f9; }
        input { flex: 1; padding: 12px 18px; border: 1px solid #ddd; border-radius: 25px; outline: none; font-size: 16px; }
        button { background: #1a5f7a; color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-weight: bold; }
        .msg { padding: 12px 16px; border-radius: 18px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; }
        .bot { background: #e8f4fd; color: #2c3e50; align-self: flex-start; border-bottom-right-radius: 2px; }
        .user { background: #1a5f7a; color: white; align-self: flex-end; border-bottom-left-radius: 2px; }
        .loading { font-style: italic; color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="chat-card">
        <div class="header">
            <h2 style="margin:0;">مساعد تاوريرت الذكي 🇲🇦</h2>
            <p style="margin:5px 0 0; font-size:13px; opacity:0.9;">خبير في الوثائق والمساطر الإدارية</p>
        </div>
        <div id="chatBox" class="chat-box">
            <div class="msg bot">مرحباً بك! تم تحديث النظام بنجاح. كيف يمكنني مساعدتك في مساطر تاوريرت اليوم؟</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="اسألني عن أي وثيقة...">
            <button onclick="askBot()">إرسال</button>
        </div>
    </div>

    <script>
        async function askBot() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const userMsg = input.value.trim();
            if (!userMsg) return;

            chatBox.innerHTML += `<div class="msg user">${userMsg}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatBox.innerHTML += `<div class="msg bot loading" id="${loadingId}">جاري التفكير...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: userMsg})
                });
                const data = await response.json();
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="msg bot">${data.answer.replace(/\\n/g, '<br>')}</div>`;
            } catch (e) {
                document.getElementById(loadingId).innerText = "حدث خطأ. يرجى المحاولة لاحقاً.";
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        document.getElementById('userInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') askBot();
        });
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
        # تعليمات دقيقة للنظام
        system_context = "أجب كخبير إداري مغربي يساعد سكان مدينة تاوريرت. اذكر الوثائق المطلوبة بدقة وبنقاط واضحة. السؤال هو: "
        
        # تغيير طريقة الاستدعاء لتجنب الأخطاء
        response = model.generate_content(system_context + user_prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({'answer': "عذراً، يرجى تحديث الصفحة والمحاولة مرة أخرى."})

if __name__ == "__main__":
    app.run()
    
