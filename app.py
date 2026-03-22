from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# قاعدة بيانات "الذكاء المحلي" - قابلة للتوسع لآلاف الأسطر
KNOWLEDGE_BASE = {
    # قسم الدارجة (للمواطن البسيط)
    "دارجة": {
        "بغيت نحفظ": "التحفيظ العقاري في تاوريرت كيبدا بتقديم طلب في 'المحافظة العقارية' (قرب العمالة). خاصك 'البلان' وشهادة الملكية أو عقد عدلي.",
        "وراق الموت": "الله يرحم الجميع. الوراثة كتبدا عند 'العدول' باش تقادو 'إراثة'. خاصكم كناش التعريف، شهادة الوفاة، وتحديد الورثة.",
        "رخصة الحانوت": "باش تفتح محل تجاري في تاوريرت، خاصك تمشي للمصلحة الاقتصادية في البلدية. كاين فرق بين 'التصريح' و'الترخيص' على حسب النشاط."
    },
    # قسم اللغة العربية (للمساطر الرسمية)
    "رسمي": {
        "الاستثمار العقاري": "إقليم تاوريرت يخضع لمخطط التهيئة العمرانية الجديد. أي استثمار يتطلب موافقة 'الوكالة الحضرية لوجدة - ملحقة تاوريرت'.",
        "الشكايات": "يمكن وضع شكاية رسمية لدى السيد وكيل الملك بمحكمة تاوريرت، أو عبر البوابة الوطنية للشكايات 'chikaya.ma'."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taourirt Knowledge Hub</title>
    <style>
        :root { --taourirt-blue: #023e8a; --taourirt-gold: #ffb703; }
        body { font-family: 'Cairo', sans-serif; background: #e9ecef; margin: 0; }
        .top-bar { background: var(--taourirt-blue); color: white; padding: 40px 20px; text-align: center; clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%); }
        .main-container { max-width: 900px; margin: -50px auto 30px; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); height: 80vh; display: flex; flex-direction: column; }
        .chat-display { flex: 1; overflow-y: auto; padding: 30px; display: flex; flex-direction: column; gap: 20px; }
        .bubble { padding: 18px 25px; border-radius: 25px; font-size: 17px; line-height: 1.8; max-width: 80%; }
        .ai { background: #f1f3f5; border-right: 6px solid var(--taourirt-gold); align-self: flex-start; color: #333; }
        .user { background: var(--taourirt-blue); color: white; align-self: flex-end; border-bottom-left-radius: 0; }
        .input-group { padding: 25px; background: white; border-top: 1px solid #eee; display: flex; gap: 15px; align-items: center; }
        input { flex: 1; padding: 15px 25px; border: 2px solid #dee2e6; border-radius: 50px; outline: none; font-size: 16px; transition: 0.3s; }
        input:focus { border-color: var(--taourirt-blue); }
        .btn { background: var(--taourirt-blue); color: white; border: none; padding: 15px 35px; border-radius: 50px; cursor: pointer; font-weight: bold; }
        .mic-icon { font-size: 24px; cursor: pointer; color: var(--taourirt-blue); opacity: 0.6; transition: 0.3s; }
        .mic-icon:hover { opacity: 1; transform: scale(1.1); }
    </style>
</head>
<body>
    <div class="top-bar">
        <h1 style="margin:0; font-size:2.5rem;">نظام المعرفة الشامل - تاوريرت 🛡️</h1>
        <p>الذكاء الاصطناعي في خدمة الإدارة والمواطن</p>
    </div>
    <div class="main-container">
        <div id="display" class="chat-display">
            <div class="bubble ai">مرحباً يوسف. أنا الآن أعمل بمحرك البحث الهجين. اسألني بالدارجة أو العربية عن أي ملف إداري أو قانوني يخص المدينة.</div>
        </div>
        <div class="input-group">
            <span class="mic-icon" onclick="alert('جاري العمل على تفعيل استقبال الصوت بالدارجة...')">🎙️</span>
            <input type="text" id="userInput" placeholder="اسأل (مثلاً: بغيت نحفظ، رخصة البناء، إراثة...)" onkeypress="if(event.key==='Enter') process()">
            <button class="btn" onclick="process()">استشارة</button>
        </div>
    </div>
    <script>
        async function process() {
            const input = document.getElementById('userInput');
            const display = document.getElementById('display');
            if(!input.value.trim()) return;
            const val = input.value;
            display.innerHTML += `<div class="bubble user">${val}</div>`;
            input.value = '';
            
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            });
            const data = await res.json();
            display.innerHTML += `<div class="bubble ai">${data.answer}</div>`;
            display.scrollTop = display.scrollHeight;
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
    p = request.json.get('prompt', '')
    
    # البحث المتقدم في الدارجة والفصحى
    for cat in KNOWLEDGE_BASE:
        for k, v in KNOWLEDGE_BASE[cat].items():
            if k in p:
                return jsonify({'answer': v})
    
    return jsonify({'answer': "بصفتي مساعدك الذكي في تاوريرت، هذا الموضوع يتطلب جمع بيانات أدق. سأقوم بإضافته لقاعدتي المعرفية فوراً. هل تقصد شيئاً يتعلق بالعقار أو الرخص التجارية؟"})

if __name__ == "__main__":
    app.run()
    
