"""Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

Example 1:

Input: nums = [2,2,1]

Output: 1

Example 2:

Input: nums = [4,1,2,1,2]

Output: 4

Example 3:

Input: nums = [1]

Output: 1"""

def FindSingle(numbers):
    nums = { }
    for i in numbers:
        if i not in nums:
            nums[i] = 1
        else:
            nums[i] += 1
    
    for key in nums:
        if nums[key] == 1:
            return key

def SingleNumber(numbers):
    result = 0
    for num in numbers:
        result = num ^ result
    
    return result

print(FindSingle([4,1,2,1,2]))
print(SingleNumber([4,1,2,1,2]))
