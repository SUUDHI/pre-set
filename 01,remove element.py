nums = [1,2,2,3,2,4]
val = 2

def remove_element(nums, val):
    for num in nums[:]:
        if num == val:
            nums.remove(num)
    return len(nums), nums

print(remove_element(nums, val))

def remove_element_1(nums, val):
    count = 0
    for num in range(len(nums)):
        if nums[num] != val:
            nums[count] = nums[num]
            count += 1

    return count, nums

print(remove_element_1(nums, val))

def removeElement_2(nums, val):
        num = 0
        while num < len(nums):
            if nums[num] == val:
                nums.pop(num)
            else:
                num += 1
        return len(nums), nums

print(removeElement_2(nums,val))
