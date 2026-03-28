import json

with open('faq.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

pairs = [[item['question'], item['answer']] for item in data]

with open('faq_data_inline.py', 'w', encoding='utf-8') as f:
    f.write('FAQ_DATA = ')
    f.write(json.dumps(pairs, ensure_ascii=False, indent=2))
    f.write('\n')

print('Done:', len(pairs), 'items')
