#Find the first duplicate and first non-duplicate element

elements = [1,2,3,4,3,4]

count = {}

for element in elements:
    if element not in count:
        count[element] = 1
    else:
        count[element] += 1

print(count)

first_non_duplicate = None

for element in elements:
    if count[element] == 1:
        first_non_duplicate = element
        break

first_duplicate = None

for element in elements:
    if count[element] > 1:
        first_duplicate = element
        break

print(first_duplicate)
print(first_non_duplicate)
