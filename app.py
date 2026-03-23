import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def search_logic(user_query):
    # تحويل النص لمدار صغير وحذف الفراغات
    user_query = user_query.lower().strip()
    if not user_query: return None
    
    try:
        # الربط مع مجلد national الذي أنشأته
        json_path = os.path.join('national', 'solutions.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for item in data['solutions']:
                # البحث في الكلمات المفتاحية والعنوان معاً
                search_content = " ".join(item['keywords']) + " " + item['title'].lower()
                
                # إذا كانت كلمة المستخدم موجودة في محتوى الحل
                if user_query in search_content:
                    return item
    except Exception as e:
        print(f"Error reading from national folder: {e}")
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
    
