#Write a function that swaps keys and values in a dictionary.

dict1 = {'a': 1, 'b': 2, 'c': 3,'d':3}

dict2 = {value: key for key, value in dict1.items()}
print(dict2)