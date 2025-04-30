# MAX SUB ARRAY
#Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
#Output: 6
#Explanation: The subarray [4,-1,2,1] has the largest sum 6.

nums = [-2,1,-3,4,-1,2,1,-5,4]

max_sum = nums[0]
sum = 0 
for num in nums:
    if sum < 0:
        sum = 0
    sum += num

    if sum > max_sum:
        max_sum = sum

print(max_sum)
