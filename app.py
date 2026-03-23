import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_logic(user_query):
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    try:
        # التعديل هنا: استخدام الاسم الصحيح للملف في مجلد national
        json_path = os.path.join('national', 'emergency_solutions.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # التأكد من البحث في قائمة "solutions" داخل الملف
            for item in data.get('solutions', []):
                # البحث في الكلمات المفتاحية والعنوان
                search_content = " ".join(item.get('keywords', [])) + " " + item.get('title', '').lower()
                
                # البحث عن أي كلمة من كلمات المستخدم
                user_words = user_query.split()
                if any(word in search_content for word in user_words):
                    return item
    except Exception as e:
        print(f"Error reading national/emergency_solutions.json: {e}")
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('prompt', '')
    result = search_logic(query)
    
    if result:
        return jsonify({"found": True, **result})
    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True)
    
