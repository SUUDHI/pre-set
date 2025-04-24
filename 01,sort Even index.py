# Sort only the even indexed element from a given list

data = [9, 4, 6, 8, 1, 3, 2]
print(data)

even_index = []

for item in range(0,len(data)):
    if item % 2 == 0:
        even_index.append(data[item])

print(even_index)

for num_1 in range(len(even_index)):
    for num_2 in range(num_1+1, len(even_index)):
        if even_index[num_1] > even_index[num_2]:
            even_index[num_1], even_index[num_2] = even_index[num_2], even_index[num_1]

print(even_index)

insertion_index = 0

for item in range(0,len(data),2):
    data[item] = even_index[insertion_index]
    insertion_index += 1

print(data)
