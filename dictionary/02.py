#Find the key with the maximum value.

orignal_dict = {'a':22, 'b': 66, 'c':44, 'd':-55}

max_vlaue = 0
max_key = None

for key, value in orignal_dict.items():
    
    if value > max_vlaue:
        max_vlaue = value
        max_key = key
    
print(max_key)
