import json
import jsonpickle

def store_data(data):
    print('Opening file for dump')
    with open('post_data.json', 'w') as f:
        json_data = jsonpickle.encode(data, unpicklable=False)
        f.write(json_data)
    print('Dumped data')