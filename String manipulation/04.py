#Find the first non-repeating character in a string.
# Input: "aabbccdeeffg"
# Output: "d"

string = "aabbccdeeffg"

non_repeating =[]

freq = {}

for item in string:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1

for key,value in freq.items():
    if value == 1:
        non_repeating.append(key)
        break
print(non_repeating)
