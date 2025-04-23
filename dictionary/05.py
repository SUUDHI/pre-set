# Merging two Dictionaries

#using loop
d1 = {'x': 1, 'y': 2}
d2 = {'y': 3, 'z': 4}

for key, value in d2.items():
    d1[key] = value

print(d1)

#using operator (|)

dict_1 = {'x': 1, 'y': 2}
dict_2 = {'y': 3, 'z': 4}

dict_3 = dict_1 | dict_2

print(dict_3)
