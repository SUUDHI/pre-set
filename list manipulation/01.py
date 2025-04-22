# Find the most frequent element in a list [1, 2, 2, 3, 3, 3, 4, 4]

data = [1, 2, 2, 3, 3, 3, 4, 4]

freq = {}

for item in data:
    if item in freq:
        freq[item]+=1
    else:
        freq[item]=1

print(freq)

max = 0

frequent_element = None

for key,value in freq.items():
    if value > max:
        max = value
        frequent_element = key

print(frequent_element)
