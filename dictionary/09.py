# Create a Dictionary from Two Lists

# Input: keys = ['name', 'age'], values = ['Alice', 25]
# Output: {'name': 'Alice', 'age': 25}

keys = ['name', 'age']

values = ['Alice', 25]

output_dict = {}

for item in range(len(keys)):
    output_dict[keys[item]] = values[item]

print(output_dict)
