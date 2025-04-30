# 3 sum 
#Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
"""
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter."""

nums = [-1,0,1,2,-1,-4]

output = set()

n = len(nums)

for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1,n):
            if nums[i] + nums[j] + nums[k] == 0:
                triplet = tuple(sorted([nums[i],nums[j],nums[k]]))
                output.add(triplet)

result = [list(triplet) for triplet in output]
print(result)