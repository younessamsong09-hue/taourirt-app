from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <div style="text-align:center; font-family:Arial; direction:rtl; padding:50px;">
        <h1 style="color:#2c3e50;">مرحباً بك في منصة تاوريرت 🇲🇦</h1>
        <p style="font-size:1.2em;">هذا التطبيق قيد التطوير لمساعدة الساكنة في أمور الوثائق والمساطر الإدارية.</p>
        <div style="background:#f1f1f1; padding:20px; border-radius:10px; display:inline-block;">
            قريباً: ماسح الوثائق بالذكاء الاصطناعي
        </div>
    </div>
    """

if __name__ == "__main__":
    app.run()
  
