import os, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def fetch_national_data():
    all_records = []
    # المسار الصحيح لـ Vercel
    base_path = os.path.join(app.root_path, 'national')
    if os.path.exists(base_path):
        for file in os.listdir(base_path):
            if file.endswith('.json'):
                with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list): all_records.extend(data)
    return all_records

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('prompt', '').lower()
    
    # قاموس الدارجة + منطق المولد
    if any(word in user_query for word in ['اكتب', 'شكاية', 'طلب', 'تحرير']):
        return jsonify({"found": True, "results": [{"type": "generator"}]})

    # البحث الشامل
    data = fetch_national_data()
    matches = [i for i in data if user_query in str(i).lower()]
    
    if matches:
        return jsonify({"found": True, "results": matches[:5]})
    return jsonify({"found": False, "message": "لم نجد نتائج دقيقة، جرب كلمات أخرى."})

if __name__ == '__main__':
    app.run(debug=True)
    
