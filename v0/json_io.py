import json
import jsonpickle

def store_data(data,filename):
    print(f'Opening file {filename} for dump')
    with open(filename+'.json', 'w') as f:
        json_data = jsonpickle.encode(data, unpicklable=False)
        f.write(json_data)
    print('Dumped data')
    
def load_data(filename):
    print(f'Opening file {filename} for read')
    with open(filename+'.json', 'r') as f:
        data = json.load(f)
        print('Loaded data')
        return data
    