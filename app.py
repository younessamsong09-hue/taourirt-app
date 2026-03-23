import os
import json

def load_all_data():
    mega_database = {}
    base_path = 'data'
    
    # التأكد من وجود المجلد لتجنب انهيار السيرفر
    if not os.path.exists(base_path):
        return mega_database

    # الكود سيمر الآن داخل المجلدات الوطنية والمدن تلقائياً
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        mega_database.update(data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    continue
    return mega_database
    
