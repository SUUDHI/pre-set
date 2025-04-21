#Find the sum of all dictionary values.
# Input: {'x': 10, 'y': 20, 'z': 30}
# Output: 60

data = {'x': 10, 'y': 20, 'z': 30}

sum = 0

for key,value in data.items():
  sum += value

print(sum)
