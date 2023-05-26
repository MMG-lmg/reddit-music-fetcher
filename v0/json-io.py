import json
def store_data(data):
    print('Opening file for dump')
    with open('data.json', 'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4, sort_keys=True)
    print('Dumped data')