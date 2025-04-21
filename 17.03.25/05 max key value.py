#Find the key with the maximum value.
# Input: {'Alice': 88, 'Bob': 75, 'Charlie': 90}
# Output: "Charlie"

data = {'Ram': -88, 'Sham': -75, 'Rahul': -90}

max_value = float('-inf')
max_key = None

for key,value in data.items():
  if value > max_value:
   max_value = value
   max_key=key

print(max_key)
