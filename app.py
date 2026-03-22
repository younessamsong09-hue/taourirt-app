from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# قاعدة البيانات الكبرى (النواة) - هنا سنجمع مئات النصوص بالدارجة والعربية
TAOURIRT_BRAIN = {
    # قسم العقار والتعمير (الأكثر طلباً)
    "عقار": {
        "keywords": ["حفظ", "محفظة", "تحفيظ", "بلان", "أرض", "بني", "رخصة"],
        "answer": "⚖️ **منظومة العقار والتعمير:**<br>في تاوريرت، أي عملية بناء أو تحفيظ تبدأ من **الوكالة الحضرية**. <br>🔹 **بالدارجة:** إذا بغيتي تبني، ضروري 'البلان' من عند مهندس و 'الرخصة' من الجماعة. البناء بلا رخصة كايعرضك للهدم والخطية."
    },
    # قسم الوثائق الشخصية
    "هوية": {
        "keywords": ["بطاقة", "لاكارط", "باسبور", "جواز", "عقد", "إزدياد"],
        "answer": "🆔 **الوثائق التعريفية:**<br>🔹 **البطاقة الوطنية:** التوجه لمفوضية الشرطة (قرب المحطة). <br>🔹 **الجواز:** الطلب عبر passport.ma والإيداع في المقاطعة التابع لها حيك في تاوريرت."
    },
    # قسم مغاربة العالم (مهم جداً للمدينة)
    "جالية": {
        "keywords": ["برا", "الغربة", "وكالة", "قنصلية", "جالية", "إقامة"],
        "answer": "🌍 **خدمات مغاربة العالم:**<br>لإجراء أي غرض إداري من الخارج، يجب إرسال **'وكالة خاصة'** مصادق عليها. <br>🔹 **نصيحة:** يمكنكم طلب 'عقد الازدياد' و 'السجل العدلي' إلكترونياً عبر البوابات الرسمية دون عناء السفر."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة تاوريرت الذكية | Taourirt Smart Hub</title>
    <style>
        :root { --primary: #0f172a; --gold: #b45309; --bg: #f8fafc; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); margin: 0; padding: 0; }
        .header { background: var(--primary); color: white; padding: 50px 20px; text-align: center; border-bottom: 5px solid var(--gold); }
        .search-container { max-width: 800px; margin: -40px auto 20px; background: white; padding: 10px; border-radius: 50px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: flex; gap: 10px; }
        input { flex: 1; border: none; padding: 15px 25px; border-radius: 50px; outline: none; font-size: 18px; }
        .btn { background: var(--gold); color: white; border: none; padding: 15px 35px; border-radius: 50px; cursor: pointer; font-weight: bold; }
        .main-content { max-width: 800px; margin: 20px auto; padding: 20px; min-height: 50vh; }
        .result-card { background: white; padding: 25px; border-radius: 15px; border-right: 8px solid var(--gold); box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; display: none; }
        .voice-section { text-align: center; padding: 20px; color: var(--slate); }
        .mic-btn { font-size: 40px; cursor: pointer; color: var(--gold); filter: grayscale(1); transition: 0.3s; }
        .mic-btn:hover { filter: grayscale(0); transform: scale(1.1); }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin:0;">بوابة المعرفة الذكية لمدينة تاوريرت 🇲🇦</h1>
        <p style="opacity:0.8;">قاعدة بيانات ضخمة بالعربية والدارجة لخدمة الساكنة</p>
    </div>

    <div class="search-container">
        <input type="text" id="query" placeholder="اسأل بالدارجة أو العربية (مثلاً: بغيت نبني، وراق الباسبور...)" onkeypress="if(event.key==='Enter') search()">
        <button class="btn" onclick="search()">بحث ذكي</button>
    </div>

    <div class="voice-section">
        <div class="mic-btn" title="خاصية البحث بالدارجة المسموعة (قيد البرمجة)">🎙️</div>
        <p><small>قريباً: تحدث بلهجتك وسيجيبك النظام</small></p>
    </div>

    <div class="main-content">
        <div id="resultCard" class="result-card"></div>
        <div id="welcomeMsg" style="text-align:center; color:#64748b;">
            <h3>أهلاً بك يا ابن مدينة تاوريرت 🛡️</h3>
            <p>ابدأ البحث عن أي مسطرة إدارية أو قانونية معقدة.</p>
        </div>
    </div>

    <script>
        async function search() {
            const val = document.getElementById('query').value.trim();
            if(!val) return;
            
            document.getElementById('welcomeMsg').style.display = 'none';
            const card = document.getElementById('resultCard');
            card.style.display = 'block';
            card.innerHTML = 'جاري تحليل البيانات الضخمة...';

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            });
            const data = await res.json();
            card.innerHTML = data.answer;
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
    
    # محرك البحث عن الكلمات المفتاحية
    for category in TAOURIRT_BRAIN.values():
        if any(keyword in prompt for keyword in category['keywords']):
            return jsonify({'answer': category['answer']})
    
    return jsonify({
        'answer': "💡 **لم نجد المعلومة بدقة بعد:** <br>نحن نقوم الآن بجمع المزيد من البيانات الضخمة حول هذا الموضوع لضمان إجابة دقيقة. جرب كلمات مثل (بناء، باسبور، حفظ)."
    })

if __name__ == "__main__":
    app.run()
    
