import json

with open('test.json','r',encoding='utf-8') as f:
    json_data = json.load(f)
# print(json_data[0])
print(json.dumps(json_data[0], indent="\t", ensure_ascii=False))