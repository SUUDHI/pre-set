#Input: nums = [2,2,1]
#Output: 1

nums = [2,2,1,3,3]

freq = {}

for num in nums:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

for key, val in freq.items():
    if val == 1:
        print (key)
