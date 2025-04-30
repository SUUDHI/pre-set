d = {
    'a': {'x': 5, 'y': 6},
    'b': {'x': 1, 'y': 4},
    'c': {'x': 8, 'y': 3}
     }

#OUTPUT : [('x', (5, 1, 8)), ('y', (6, 4, 3))]

data = {'x': [], 'y': []}

#print(data)
output = []

keys = []

for key, val in d.items():
    data['x'].append(val['x'])
    data['y'].append(val['y'])

print(data)
