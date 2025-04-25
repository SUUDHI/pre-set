d = {
    'gfg': {'x': 5, 'y': 6}, 
    'is': {'x': 1, 'y': 4}, 
    'best': {'x': 8, 'y': 3}
     }

#OUTPUT : [('x', (5, 1, 8)), ('y', (6, 4, 3))]

#print(d)

key_list = []

for val in d.values():
    key_list.append(val)

#print(key_list)
result = {}

for i in range(len(key_list)):
    current_dict = key_list[i]
    for key in current_dict:
        if key not in result:
            result[key] = []
        result[key].append(current_dict[key])
        
print(result)

final_output = []
for key in result:
    final_output.append((key, tuple(result[key])))

print(final_output)
