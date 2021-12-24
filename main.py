import json 



with open('test.json',encoding = 'utf8') as f:
    data = json.load(f)

    def search():
        return [datum for datum in data ]

    for dict in data:
        datum = search()
        print(datum['No'])