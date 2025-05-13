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
def find_insert_position(nums,target):
    length_of_nums = len(nums)
    for item in range(len(nums)):
        if target - nums[item] == 0:
            return item
        elif target - nums[item] == -1:
            return item
    else:
        return length_of_nums


def find_insert_position_2(nums,target):
    for item in range(len(nums)):
        if nums[item] >= target:
            return item
    return len(nums)


def find_insert_position_3(nums,target):
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if target == nums[mid]:
            return mid
        if target >= nums[mid]:
            left = mid + 1
        else:
            right = mid - 1

    return left 

nums = [1,3,5,6]
target = 7

print(find_insert_position(nums,target))
print(find_insert_position_3(nums,target))