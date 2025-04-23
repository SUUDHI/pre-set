#Character with Highest Frequency

# Input: "success"
# Output: 's'

Input = "success"

freq = {}

for i in Input:
    if i not in freq:
        freq[i] = 1
    else:
        freq[i] += 1

print(freq)

max_vlaue = 0 
max_key = None

for key, value in freq.items():
    if value > max_vlaue:
        max_vlaue = value
        max_key = key
    
print(max_key)
