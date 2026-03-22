from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; direction: rtl; text-align: center; background: #f4f7f6; padding: 20px; }
            .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
            input { width: 80%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 10px; }
            button { background: #27ae60; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            #response { margin-top: 20px; font-weight: bold; color: #2c3e50; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>منصة تاوريرت الذكية 🇲🇦</h1>
            <p>اسألني عن أي وثيقة إدارية (مثلاً: البطاقة الوطنية)</p>
            <input type="text" id="userInput" placeholder="اكتب سؤالك هنا...">
            <button onclick="askAI()">إرسال</button>
            <div id="response"></div>
        </div>

        <script>
            function askAI() {
                const input = document.getElementById('userInput').value;
                const resDiv = document.getElementById('response');
                resDiv.innerText = "جاري التفكير... (قريباً سنربطه بـ Gemini)";
                
                // هذه محاكاة بسيطة للرد
                setTimeout(() => {
                    if(input.includes("بطاقة")) {
                        resDiv.innerText = "للحصول على البطاقة الوطنية بوهدود، تحتاج إلى: 4 صور، عقد الازدياد، وشهادة السكنى.";
                    } else {
                        resDiv.innerText = "سؤال جيد! سأبحث لك عن الإجراءات الإدارية في بلدية تاوريرت.";
                    }
                }, 1000);
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
    
