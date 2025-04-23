##Write a function that swaps keys and values in a dictionary.

data = {1 : 'a', 2 : 'b', 3 : 'c'}

swap_data = {}

for key, value in data.items():
    swap_data[value] = key

print(data)
print(swap_data)

def key_value_swap(dict):
    swap_dict = {}
    
    for key, value in dict.items():
        swap_dict[value] = key
    
    return swap_dict

originl_dict = {4 : 'd', 5 : 'e', 6 : 'f'}

swap_dict = key_value_swap(originl_dict)

print(originl_dict)
print(swap_dict)