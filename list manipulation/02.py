# Find all duplicates in a list [1, 2, 3, 4, 5, 2, 3, 6]

data = [1, 2, 3, 4, 5, 2, 3, 6]

non_duplicates = []

duplicates = []

for number in data:
    if number not in non_duplicates:
        non_duplicates.append(number)
    else:
        duplicates.append(number)

print(duplicates)
