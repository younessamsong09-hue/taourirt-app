from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# قاعدة بيانات ضخمة (ستكبر مع الوقت) - تشمل العربية والدارجة
# يمكننا لاحقاً ربطها بقاعدة بيانات SQL أو NoSQL
MEGA_DATA = {
    "legal": {
        "محكمة": "المحكمة الابتدائية بتاوريرت تقع في وسط المدينة. تشمل قضاء الأسرة، الحالة المدنية، والمنازعات المدنية.",
        "عقار": "قوانين التحفيظ العقاري (قانون 14-07) هي الضامن لملكيتك في تاوريرت. ابدأ بشهادة الملكية من المحافظة.",
    },
    "darija": {
        "فين نقاد": "باش تقاد وراقك (مثل البطاقة أو الباسبور)، خاصك تمشي للمقاطعة اللي تابعة لداركم في تاوريرت أولاً.",
        "شحال كنخلص": "الواجبات كتختلف: 75 درهم للبطاقة الوطنية، و300/500 درهم للباسبور (تمبر إلكتروني).",
        "باغي نحفظ": "التحفيظ كيبدا عند المحافظة العقارية، خاصك تجيب معاك 'البلان' ديال لانسبيكتور (المهندس الطبوغرافي)."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taourirt Smart Hub | المستشار الرقمي</title>
    <style>
        :root { --main-gold: #c5a059; --bg-dark: #0a0f18; }
        body { font-family: 'Cairo', sans-serif; background: #f0f2f5; margin: 0; }
        .header { background: var(--bg-dark); color: white; padding: 40px 20px; text-align: center; border-bottom: 6px solid var(--main-gold); }
        .container { max-width: 800px; margin: -30px auto 20px; background: white; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .chat-box { flex: 1; overflow-y: auto; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 15px 20px; border-radius: 15px; max-width: 85%; font-size: 16px; line-height: 1.8; position: relative; }
        .bot { background: #f8f9fa; border-right: 5px solid var(--main-gold); align-self: flex-start; }
        .user { background: var(--bg-dark); color: white; align-self: flex-end; }
        .input-area { padding: 20px; background: #fff; border-top: 1px solid #eee; display: flex; gap: 10px; }
        input { flex: 1; padding: 15px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 16px; outline: none; }
        button { background: var(--main-gold); color: white; border: none; padding: 0 25px; border-radius: 12px; cursor: pointer; font-weight: bold; }
        .voice-btn { background: #e2e8f0; color: #1e293b; padding: 10px; border-radius: 50%; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin:0;">منظومة تاوريرت المعرفية 🇲🇦</h1>
        <p>مستشارك الذكي باللغة العربية والدارجة</p>
    </div>
    <div class="container">
        <div id="chatBox" class="chat-box">
            <div class="msg bot">مرحباً بك في النواة الأولى لنظام الذكاء الاصطناعي لمدينة تاوريرت. يمكنك الكتابة بالعربية الفصحى أو "الدارجة".</div>
        </div>
        <div class="input-area">
            <button class="voice-btn" title="قريباً: التحدث بالدارجة">🎤</button>
            <input type="text" id="userInput" placeholder="اسألني أي شيء (عربية أو دارجة)..." onkeypress="if(event.key==='Enter') ask()">
            <button onclick="ask()">بحث</button>
        </div>
    </div>
    <script>
        async function ask() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            if(!input.value.trim()) return;
            const text = input.value;
            chatBox.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: text})
            });
            const data = await response.json();
            chatBox.innerHTML += `<div class="msg bot">${data.answer}</div>`;
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
    user_prompt = request.json.get('prompt', '').strip()
    
    # محرك البحث الذكي (يغطي الدارجة والعربية)
    answer = "هذه المعلومة سيتم إضافتها قريباً للقاعدة الضخمة. نحن نجمع الآن كل المعطيات القانونية لتاوريرت."
    
    # دمج البحث في كل البيانات
    for category in MEGA_DATA.values():
        for key, val in category.items():
            if key in user_prompt.lower():
                answer = val
                break
                
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run()
    
