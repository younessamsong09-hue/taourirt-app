from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# قاعدة البيانات الضخمة - "مرجع تاوريرت السيادي"
# يمكنك إضافة مئات الخدمات هنا بنفس التنسيق
SERVICES_DATABASE = {
    "البطاقة الوطنية": {
        "keywords": ["لاكارط", "بطاقة", "هوية", "cin"],
        "docs": "شهادة السكنى (من الأمن)، عقد الازدياد، 4 صور خلفية رمادية.",
        "cost": "75 درهم (تمبر إلكتروني).",
        "time": "من 10 إلى 15 يوم عمل.",
        "location": "المنطقة الإقليمية للأمن (قرب محطة القطار القديمة)."
    },
    "جواز السفر": {
        "keywords": ["باسبور", "سفر", "passport"],
        "docs": "بطاقة التعريف الوطنية الأصلية، تمبر إلكتروني، صورتان فوتوغرافيتان.",
        "cost": "300 درهم للصغار / 500 درهم للكبار.",
        "time": "7 إلى 10 أيام.",
        "location": "الملحقة الإدارية (المقاطعة) التابع لها محل سكنك."
    },
    "رخصة البناء": {
        "keywords": ["بني", "بلان", "رخصة", "تعمير"],
        "docs": "تصميم معماري، شهادة الملكية، تصميم طبوغرافي، كناش التحملات.",
        "cost": "تختلف حسب المساحة (رسوم جماعية + واجبات الوكالة الحضرية).",
        "time": "شهر إلى شهرين (حسب اللجنة).",
        "location": "قسم التعمير بالجماعة الحضرية + الوكالة الحضرية."
    },
    "تصحيح الإمضاء": {
        "keywords": ["إمضاء", "سينيي", "ليغاليزي", "legalisation"],
        "docs": "الوثيقة الأصلية + بطاقة التعريف الوطنية.",
        "cost": "2 درهم (تمبر) لكل نسخة.",
        "time": "فوري (في الحين).",
        "location": "أقرب ملحقة إدارية أو مقر البلدية."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دليل تاوريرت الإداري الشامل</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #0f172a; --gold: #b45309; --bg: #f1f5f9; }
        body { font-family: 'Cairo', sans-serif; background: var(--bg); margin: 0; color: var(--primary); }
        .header { background: var(--primary); color: white; padding: 50px 20px; text-align: center; border-bottom: 5px solid var(--gold); }
        .container { max-width: 900px; margin: -40px auto 40px; padding: 0 15px; }
        .search-card { background: white; padding: 10px; border-radius: 50px; display: flex; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 2px solid var(--gold); }
        input { flex: 1; border: none; padding: 15px 25px; border-radius: 50px; outline: none; font-size: 18px; font-family: 'Cairo'; }
        .btn { background: var(--primary); color: white; border: none; padding: 0 40px; border-radius: 50px; cursor: pointer; font-weight: bold; }
        .result-box { margin-top: 30px; display: none; }
        .info-card { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border-right: 10px solid var(--gold); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .item { background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; }
        .label { font-weight: bold; color: var(--gold); display: block; margin-bottom: 5px; font-size: 14px; }
        .value { font-size: 16px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="header">
        <h1>موسوعة خدمات تاوريرت 🛡️</h1>
        <p>كل ما تحتاجه (الوثائق، الوقت، التكلفة، المكان) في مكان واحد</p>
    </div>

    <div class="container">
        <div class="search-card">
            <input type="text" id="userInput" placeholder="ابحث عن خدمة (مثلاً: لاكارط، باسبور، رخصة البناء...)" onkeypress="if(event.key==='Enter') search()">
            <button class="btn" onclick="search()">بحث</button>
        </div>

        <div id="resultBox" class="result-box">
            <div class="info-card">
                <h2 id="serviceTitle" style="margin-top:0; color:var(--primary);"></h2>
                <div class="grid">
                    <div class="item"><span class="label">📄 الوثائق المطلوبة:</span><span id="docs" class="value"></span></div>
                    <div class="item"><span class="label">💰 التكلفة التقديرية:</span><span id="cost" class="value"></span></div>
                    <div class="item"><span class="label">⏳ الوقت المتوقع:</span><span id="time" class="value"></span></div>
                    <div class="item"><span class="label">📍 المكان في تاوريرت:</span><span id="loc" class="value"></span></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function search() {
            const val = document.getElementById('userInput').value.trim();
            if(!val) return;

            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: val})
            });
            const data = await res.json();

            if(data.found) {
                document.getElementById('resultBox').style.display = 'block';
                document.getElementById('serviceTitle').innerText = data.title;
                document.getElementById('docs').innerText = data.docs;
                document.getElementById('cost').innerText = data.cost;
                document.getElementById('time').innerText = data.time;
                document.getElementById('loc').innerText = data.location;
            } else {
                alert("المعذرة، هذه الخدمة جاري إضافتها للقاعدة. جرب كلمات أخرى.");
            }
        }
    </script>
</body>
</html>
