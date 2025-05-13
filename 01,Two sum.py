# Example 1:

# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].



# output = []
# for i in range(len(nums)):
#     for j in range(i,len(nums)):
#         if nums[i] + nums[j] == 9:
#             output.append(nums[i])
#             output.append(nums[j])

# print(output)

#using two loops,
def Target_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i,len(nums)):
            if nums[i] + nums[j] == target:
                return [nums[i], nums[j]]
            
 # using single loop,   
def Target_sum_2(nums, target):
    for i in range(len(nums)):
        diff = target - nums[i]
        if diff in nums:
            return [nums[i], diff]

nums = [1,4,6,8]
target = 5

print(Target_sum_2(nums,target))

print(Target_sum(nums,target))

#using dict
def two_sun(nums,target):
    complement = {}

    for i in range(len(nums)):
        num = nums[i]
        diff = target - nums[i]
        
        if num in complement:
            return [complement[num], i]
        else:
            complement[diff] = i

print(two_sun(nums, target)) 
