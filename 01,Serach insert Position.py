"""
Given a sorted array of distinct integers and a target value, return the index if the target is found.
If not, return the index where it would be if it were inserted in order.
You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2
Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1
Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4

"""
def target(nums,t):
    k = len(nums)
    for i in range(len(nums)):
        if t - nums[i] == 0:
            return i
        elif t - nums[i] == -1:
            return i
    else:
        return k


def target2(nums,t):
    for i in range(len(nums)):
        if nums[i] >= t:
            return i
    return len(nums)


def target3(nums,t):
    l = 0
    r = len(nums) - 1
    
    while l <= r:
        mid = (l + r) // 2
        
        if t == nums[mid]:
            return mid
        if t >= nums[mid]:
            l = mid + 1
        else:
            r = mid - 1

    return l 

nums = [1,3,5,6]
t = 7

print(target(nums,t))
print(target3(nums,t))