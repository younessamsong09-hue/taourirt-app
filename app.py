def search_in_json(query):
    query = query.lower().strip() # تنظيف النص من الفراغات
    try:
        with open('data/solutions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data['solutions']:
                # البحث في العنوان وفي الكلمات المفتاحية
                combined_text = " ".join(item['keywords']) + " " + item['title'].lower()
                
                # إذا كانت أي كلمة من كلمات المستخدم موجودة في قاعدة البيانات
                user_words = query.split()
                if any(word in combined_text for word in user_words):
                    return item
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return None
    return None
    
