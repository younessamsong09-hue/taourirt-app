from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# قاعدة بيانات الحلول الإدارية المعقدة (مركز الخبرة)
EXPERT_SYSTEM = {
    "التحفيظ": "🛡️ **حماية الملكية العقارية:**<br>إذا كانت الأرض غير محفظة، فالبداية من 'مطلب التحفيظ' لدى المحافظة العقارية بتاوريرت. ستحتاج لبيان مساحي (Plan) من مهندس طبوغرافي معتمد. <br>⚠️ **تنبيه:** تأكد من عدم وجود 'تعرضات' في الجريدة الرسمية.",
    "الوكالة": "🌍 **خدمة مغاربة العالم:**<br>لإجراء معاملة في تاوريرت وأنت بالخارج، يجب إعداد 'وكالة خاصة' مصادق عليها في القنصلية. <br>📍 **نصيحة:** حدد نوع التصرف بدقة (بيع، شراء، سحب وثائق) لتجنب رفضها إدارياً.",
    "التعمير": "🏗️ **قانون التعمير (12-90):**<br>بناء مستودع أو منزل يتطلب رخصة بناء حصراً. البناء العشوائي في ضواحي تاوريرت يعرضك لغرامات ثقيلة وهدم المنشأة. ابدأ دائماً بالمنصة الرقمية 'rokhas.ma'.",
    "عقد الكراء": "📝 **تحصين الكراء:**<br>لا تكتفِ بتصحيح الإمضاء! يجب تسجيل عقد الكراء لدى إدارة الضرائب لضمان حقوقك في الإفراغ أو استرجاع المستحقات أمام المحكمة الابتدائية بتاوريرت."
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة تاوريرت للخدمات الرقمية</title>
    <style>
        :root { --legal-blue: #1e293b; --royal-gold: #d4af37; --success: #059669; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; margin: 0; color: #1e293b; }
        .sidebar-layout { display: flex; min-height: 100vh; }
        .main-content { flex: 1; max-width: 800px; margin: 20px auto; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #e2e8f0; }
        .hero-header { background: var(--legal-blue); color: white; padding: 30px; border-bottom: 5px solid var(--royal-gold); }
        .badge { background: var(--royal-gold); color: black; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
        .chat-window { flex: 1; overflow-y: auto; padding: 25px; background: #ffffff; min-height: 400px; }
        .msg { margin-bottom: 20px; padding: 15px 20px; border-radius: 12px; font-size: 15px; line-height: 1.8; max-width: 85%; }
        .ai-response { background: #f1f5f9; border-right: 5px solid var(--royal-gold); align-self: flex-start; }
        .user-query { background: var(--legal-blue); color: white; align-self: flex-end; border-bottom-left-radius: 2px; margin-right: auto; }
        .input-zone { padding: 20px; background: #f8fafc; display: flex; gap: 12px; border-top: 1px solid #eee; }
        input { flex: 1; padding: 15px; border-radius: 8px; border: 2px solid #e2e8f0; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--royal-gold); }
        .btn-send { background: var(--legal-blue); color: white; border: none; padding: 0 30px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-send:hover { background: #0f172a; }
        .quick-links { display: flex; flex-wrap: wrap; gap: 10px; padding: 0 25px 20px; }
        .chip { background: #f1f5f9; padding: 8px 15px; border-radius: 6px; font-size: 13px; cursor: pointer; border: 1px solid #cbd5e1; }
        .chip:hover { background: var(--royal-gold); color: white; border-color: var(--royal-gold); }
    </style>
</head>
<body>
    <div class="main-content">
        <div class="hero-header">
            <span class="badge">Official Platform</span>
            <h1 style="margin:10px 0 5px;">منصة تاوريرت للتوجيه القانوني والإداري</h1>
            <p style="margin:0; opacity:0.8; font-size:13px;">النظام المرجعي الأول للمواطن والمستثمر بإقليم تاوريرت</p>
        </div>

        <div id="chatBox" class="chat-window">
            <div class="msg ai-response">
                مرحباً بك في المركز الرقمي الموحد. <br>
                لقد قمنا بتطوير هذا النظام لتقديم استشارات دقيقة حول <strong>المساطر العقارية، التراخيص التجارية، وخدمات مغاربة العالم</strong>. <br>
                بماذا يمكنني خدمتك بشكل معمق اليوم؟
            </div>
        </div>

        <div class="quick-links">
            <div class="chip" onclick="ask('التحفيظ العقاري')">⚖️ قضايا التحفيظ</div>
            <div class="chip" onclick="ask('رخصة التعمير')">🏗️ رخص البناء</div>
            <div class="chip" onclick="ask('الوكالة')">🌍 خدمات الجالية</div>
            <div class="chip" onclick="ask('عقد الكراء')">📝 توثيق العقود</div>
        </div>

        <div class="input-zone">
            <input type="text" id="userInput" placeholder="اكتب موضوعك الإداري هنا..." onkeypress="if(event.key==='Enter') ask()">
            <button class="btn-send" onclick="ask()">استشارة</button>
        </div>
    </div>

    <script>
        function ask(query = null) {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const val = query || input.value.trim();
            if(!val) return;

            chatBox.innerHTML += `<div class="msg user-query">${val}</div>`;
            if(!query) input.value = '';
            
            fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            })
            .then(res => res.json())
            .then(data => {
                chatBox.innerHTML += `<div class="msg ai-response">${data.answer}</div>`;
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
    prompt = request.json.get('prompt', '').lower()
    
    # محرك البحث عن الحلول
    for key in EXPERT_SYSTEM:
        if key in prompt:
            return jsonify({'answer': EXPERT_SYSTEM[key]})
    
    return jsonify({
        'answer': "هذا الملف يتطلب تدقيقاً في <strong>القوانين التنظيمية المعمول بها بجماعة تاوريرت</strong>. هل تود أن أوجهك للمصلحة الخارجية المختصة (العمالة، المحكمة، أو البلدية) مع قائمة الوثائق التقنية؟"
    })

if __name__ == "__main__":
    app.run()
    
