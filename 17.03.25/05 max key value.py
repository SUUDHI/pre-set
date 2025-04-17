#Find the key with the maximum value.
# Input: {'Alice': 88, 'Bob': 75, 'Charlie': 90}
# Output: "Charlie"

dic = {'Ram': 88, 'Sham': 75, 'Rahul': 90}
max_value=0
max_key = None
for key,value in dic.items():
  if value > max_value:
   max_value = value
   max_key=key
print(max_key)
