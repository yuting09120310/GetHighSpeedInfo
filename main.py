import json 

with open('2021_12_23.json',encoding = 'utf8') as f:
    data = json.load(f)
print(data)