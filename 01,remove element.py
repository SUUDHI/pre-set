nums = [1,2,2,3,2,4]
val = 2

def remove_element(nums, val):
    for i in nums[:]:
        if i == val:
            nums.remove(i)
    return len(nums), nums

print(remove_element(nums, val))

def re(nums, val):
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1

    return k, nums

print(re(nums, val))

def removeElement(nums, val):
        i = 0
        while i < len(nums):
            if nums[i] == val:
                nums.pop(i)
            else:
                i += 1
        return len(nums), nums

print(removeElement(nums,val))
