#Write a function that swaps keys and values in a dictionary.

data = {'a': 1, 'b': 2, 'c': 3,'d':3}

swap_data = {value: key for key, value in data.items()}

print(swap_data)
